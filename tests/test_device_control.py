from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from integrations.device_control.discovery import AuthorizedNetworkPolicy, send_wol
from integrations.device_control.manager import DeviceControlManager
from integrations.device_control.models import NetworkDevice, StateConfidence


class TestDeviceControl(unittest.TestCase):
    def test_authorized_network_policy(self):
        policy = AuthorizedNetworkPolicy(["192.168.1.0/24"])
        self.assertTrue(policy.is_ip_authorized("192.168.1.45"))
        self.assertFalse(policy.is_ip_authorized("192.168.2.45"))
        self.assertFalse(policy.is_ip_authorized("8.8.8.8"))
        self.assertFalse(policy.is_ip_authorized("invalid-ip"))

    def test_send_wol_validation_and_packet(self):
        ok, _ = send_wol("not-a-mac")
        self.assertFalse(ok)
        with patch("socket.socket") as mock_sock:
            inst = mock_sock.return_value.__enter__.return_value
            ok2, _ = send_wol("AA:BB:CC:DD:EE:FF")
            self.assertTrue(ok2)
            sent_bytes, addr = inst.sendto.call_args[0]
            self.assertEqual(len(sent_bytes), 102)
            self.assertEqual(sent_bytes[:6], b"\xff" * 6)
            self.assertEqual(addr[1], 9)

    def test_manager_pairing_and_offline_confidence(self):
        with tempfile.TemporaryDirectory() as td:
            mgr = DeviceControlManager(
                state_file=Path(td) / "state.json",
                creds_file=Path(td) / "creds.enc",
            )
            dev = NetworkDevice(
                id="lan_roku_192_168_1_50",
                name="TV Sala Roku",
                ip="192.168.1.50",
                mac="AA:BB:CC:DD:EE:FF",
                category="tv",
                protocol="roku",
                port=8060,
                room="Sala",
                online=True,
                state={"power": True},
                state_confidence=StateConfidence.CONFIRMED.value,
            )
            mgr._discovered[dev.id] = dev

            # Must require pairing before control
            ok, msg = mgr.control_device(dev.id, "volume_up")
            self.assertFalse(ok)
            self.assertIn("emparejado", msg.lower())

            # Pair device
            ok_p, _ = mgr.authorize_and_pair(dev.id, custom_name="Roku Sala", room="Sala")
            self.assertTrue(ok_p)

            # Simulate unreachable device on refresh: must become UNKNOWN, NOT power=False
            with patch("integrations.device_control.adapters.RokuAdapter.refresh_state", return_value=(False, {"power": True}, StateConfidence.UNKNOWN.value)):
                ref_ok, updated = mgr.refresh_device(dev.id)
                self.assertFalse(ref_ok)
                self.assertIsNotNone(updated)
                self.assertFalse(updated.online)
                self.assertEqual(updated.state_confidence, StateConfidence.UNKNOWN.value)
                self.assertTrue(updated.state.get("power"))

    def test_scene_confirmation_gate(self):
        with tempfile.TemporaryDirectory() as td:
            mgr = DeviceControlManager(
                state_file=Path(td) / "state.json",
                creds_file=Path(td) / "creds.enc",
            )
            ok_no, msg = mgr.execute_scene("apagado_general", confirmed=False)
            self.assertFalse(ok_no)
            self.assertIn("confirma", msg.lower())

            ok_yes, _ = mgr.execute_scene("modo_cine", confirmed=True)
            self.assertTrue(ok_yes)

    def test_voice_action_ambiguity(self):
        from actions.device_control import device_control_action

        res = json.loads(device_control_action({"action": "list"}))
        self.assertTrue(res["ok"])
        amb = json.loads(device_control_action({"action": "control", "target": "Luz", "command": "power_off"}))
        self.assertFalse(amb["ok"])
        self.assertTrue(amb.get("ambiguous"))


if __name__ == "__main__":
    unittest.main()
