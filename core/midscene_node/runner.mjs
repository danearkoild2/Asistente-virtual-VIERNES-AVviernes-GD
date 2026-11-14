import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { PlaywrightAgent } from "@midscene/web/playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, "..", "..");

function ensureMidsceneEnv() {
  if (process.env.MIDSCENE_MODEL_API_KEY || process.env.OPENAI_API_KEY) {
    return;
  }
  const keyFile = path.join(ROOT_DIR, "config", "api_keys.json");
  if (!fs.existsSync(keyFile)) return;
  try {
    const raw = JSON.parse(fs.readFileSync(keyFile, "utf-8"));
    const geminiKey = (raw.gemini_api_key || "").trim();
    if (geminiKey) {
      process.env.MIDSCENE_MODEL_API_KEY = geminiKey;
      process.env.MIDSCENE_MODEL_BASE_URL =
        process.env.MIDSCENE_MODEL_BASE_URL ||
        "https://generativelanguage.googleapis.com/v1beta/openai/";
      process.env.MIDSCENE_MODEL_NAME =
        process.env.MIDSCENE_MODEL_NAME || "gemini-2.5-flash";
      process.env.MIDSCENE_MODEL_FAMILY =
        process.env.MIDSCENE_MODEL_FAMILY || "gemini";
    }
  } catch {
    // Ignore malformed config; caller will see missing key error if action requires LLM.
  }
}

async function readInputPayload() {
  if (process.argv[2]) {
    return JSON.parse(process.argv[2]);
  }
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const text = Buffer.concat(chunks).toString("utf-8").trim();
  return text ? JSON.parse(text) : {};
}

async function main() {
  ensureMidsceneEnv();
  const payload = await readInputPayload();
  const url = String(payload.url || "").trim();
  const mode = String(payload.mode || "action").trim().toLowerCase();
  const instruction = String(payload.instruction || "").trim();
  const target = String(payload.target || instruction).trim();
  const value = String(payload.value || "").trim();
  const headless = payload.headless !== false;

  if (!url) {
    console.log(JSON.stringify({ ok: false, error: "url es obligatoria" }));
    process.exit(1);
  }

  let browser;
  try {
    browser = await chromium.launch({ headless });
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await context.newPage();
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });

    const agent = new PlaywrightAgent(page);
    let result = null;

    if (mode === "query") {
      result = await agent.aiQuery(instruction || target);
    } else if (mode === "assert") {
      await agent.aiAssert(instruction);
      result = { asserted: true };
    } else if (mode === "tap") {
      await agent.aiTap(target);
      result = { tapped: target };
    } else if (mode === "input") {
      await agent.aiInput(target, { value });
      result = { inputted: target };
    } else {
      await agent.aiAction(instruction || target);
      result = { completed: true };
    }

    console.log(
      JSON.stringify({
        ok: true,
        mode,
        url: page.url(),
        title: await page.title(),
        result,
      })
    );
  } catch (err) {
    console.log(
      JSON.stringify({
        ok: false,
        mode,
        error: err?.message || String(err),
      })
    );
    process.exitCode = 1;
  } finally {
    if (browser) {
      await browser.close().catch(() => {});
    }
  }
}

main();
