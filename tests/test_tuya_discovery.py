#!/usr/bin/env python3
# encoding: utf-8
"""
Tests for tuya-discovery.py - UDP device discovery service

This test suite covers:
- Device discovery via UDP broadcasts on ports 6666/6667
- Encrypted and unencrypted message handling
- Duplicate device filtering
- JSON parsing and device type detection
- ESP vs non-ESP device identification
"""

import asyncio
import json
import os
import sys
from hashlib import md5
from unittest.mock import Mock, patch

import pytest

# Import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "tuya_discovery",
    os.path.join(os.path.dirname(__file__), "..", "scripts", "tuya-discovery.py"),
)
tuya_discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tuya_discovery)


class TestUDPKeyGeneration:
    """Test UDP decryption key generation."""

    def test_udp_key_derived_from_magic_string(self):
        """Test that UDP key is MD5 hash of magic string."""
        expected_key = md5(b"yGAdlopoPVldABfn").digest()
        assert tuya_discovery.udpkey == expected_key

    def test_udp_key_length(self):
        """Test that UDP key is 16 bytes (AES-128)."""
        assert len(tuya_discovery.udpkey) == 16

    def test_udp_key_is_bytes(self):
        """Test that UDP key is bytes type."""
        assert isinstance(tuya_discovery.udpkey, bytes)


class TestDecryptUDPFunction:
    """Test UDP message decryption."""

    def test_decrypt_udp_function_exists(self):
        """Test that decrypt_udp lambda is defined."""
        assert callable(tuya_discovery.decrypt_udp)

    def test_decrypt_udp_uses_correct_key(self):
        """Test that decrypt_udp uses the UDP key."""
        from crypto_utils import encrypt

        # Create a test message
        test_message = "test message"
        encrypted = encrypt(test_message, tuya_discovery.udpkey)

        # Decrypt using the lambda
        decrypted = tuya_discovery.decrypt_udp(encrypted)

        assert decrypted == test_message


class TestTuyaDiscoveryProtocol:
    """Test TuyaDiscovery asyncio DatagramProtocol."""

    def setup_method(self):
        """Reset devices_seen set before each test."""
        tuya_discovery.devices_seen.clear()

    def test_protocol_instantiation(self):
        """Test that TuyaDiscovery protocol can be instantiated."""
        protocol = tuya_discovery.TuyaDiscovery()
        assert isinstance(protocol, asyncio.DatagramProtocol)

    def test_datagram_received_exists(self):
        """Test that datagram_received method exists."""
        protocol = tuya_discovery.TuyaDiscovery()
        assert hasattr(protocol, "datagram_received")
        assert callable(protocol.datagram_received)


class TestDatagramReceivedUnencrypted:
    """Test receiving unencrypted UDP broadcasts."""

    def setup_method(self):
        """Reset devices_seen set before each test."""
        tuya_discovery.devices_seen.clear()

    def test_receives_unencrypted_broadcast(self):
        """Test receiving unencrypted device broadcast."""
        protocol = tuya_discovery.TuyaDiscovery()

        # Create test data with proper framing (20 bytes header + data + 8 bytes footer)
        device_info = json.dumps({"ip": "10.42.42.42", "gwId": "12345678901234567890"})
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + device_info.encode() + footer

        addr = ("10.42.42.42", 6666)

        with patch("builtins.print"):
            protocol.datagram_received(data, addr)

        # Device should be added to seen set
        assert data in tuya_discovery.devices_seen

    def test_ignores_duplicate_broadcasts(self):
        """Test that duplicate broadcasts are ignored."""
        protocol = tuya_discovery.TuyaDiscovery()

        device_info = json.dumps({"ip": "10.42.42.42"})
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + device_info.encode() + footer
        addr = ("10.42.42.42", 6666)

        # Add to seen devices
        tuya_discovery.devices_seen.add(data)

        with patch("builtins.print") as mock_print:
            protocol.datagram_received(data, addr)

        # Print should not be called for duplicate
        assert not mock_print.called

    def test_parses_device_json(self):
        """Test that device JSON is parsed correctly."""
        protocol = tuya_discovery.TuyaDiscovery()

        device_data = {"ip": "10.42.42.42", "gwId": "test123", "ability": 1}
        device_info = json.dumps(device_data)
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + device_info.encode() + footer
        addr = ("10.42.42.42", 6666)

        with patch("builtins.print") as mock_print:
            protocol.datagram_received(data, addr)

        # Should print IP and data
        assert mock_print.call_count >= 1


class TestDatagramReceivedEncrypted:
    """Test receiving encrypted UDP broadcasts."""

    def setup_method(self):
        """Reset devices_seen set before each test."""
        tuya_discovery.devices_seen.clear()

    def test_receives_encrypted_broadcast(self):
        """Test receiving encrypted device broadcast."""
        from crypto_utils import encrypt

        protocol = tuya_discovery.TuyaDiscovery()

        # Create encrypted data
        device_info = json.dumps({"ip": "10.42.42.42", "gwId": "encrypted123"})
        encrypted_payload = encrypt(device_info, tuya_discovery.udpkey)

        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + encrypted_payload + footer

        addr = ("10.42.42.42", 6667)

        with patch("builtins.print") as mock_print:
            protocol.datagram_received(data, addr)

        # Device should be added to seen set
        assert data in tuya_discovery.devices_seen
        # Should successfully decrypt and print
        assert mock_print.called

    def test_handles_decryption_failure_gracefully(self):
        """Test that decryption failures are handled gracefully."""
        protocol = tuya_discovery.TuyaDiscovery()

        # Create malformed encrypted data that can't be decrypted
        device_info = "plain text data"
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + device_info.encode() + footer

        addr = ("10.42.42.42", 6667)

        with patch("builtins.print") as mock_print:
            # Should not raise exception
            protocol.datagram_received(data, addr)

        # Should still add to seen devices
        assert data in tuya_discovery.devices_seen


class TestESPDeviceDetection:
    """Test ESP vs non-ESP device detection via typo."""

    def setup_method(self):
        """Reset devices_seen set before each test."""
        tuya_discovery.devices_seen.clear()

    def test_detects_esp_device_with_ability(self):
        """Test detection of ESP device (correct spelling: 'ability')."""
        protocol = tuya_discovery.TuyaDiscovery()

        # ESP devices have "ability" (correct spelling)
        device_data = {"ip": "10.42.42.42", "ability": 1, "gwId": "esp8266device"}
        device_info = json.dumps(device_data)
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + device_info.encode() + footer
        addr = ("10.42.42.42", 6666)

        with patch("builtins.print") as mock_print:
            protocol.datagram_received(data, addr)

        # Should NOT print warning for ESP device
        warning_printed = any(
            "does not use an ESP82xx" in str(call) for call in mock_print.call_args_list
        )
        assert not warning_printed

    def test_detects_non_esp_device_with_typo(self):
        """Test detection of non-ESP device (typo: 'ablilty')."""
        protocol = tuya_discovery.TuyaDiscovery()

        # Non-ESP devices have "ablilty" (typo in SDK)
        device_data = {"ip": "10.42.42.42", "ablilty": 1, "gwId": "nonespdevice"}
        device_info = json.dumps(device_data)
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + device_info.encode() + footer
        addr = ("10.42.42.42", 6666)

        with patch("builtins.print") as mock_print:
            protocol.datagram_received(data, addr)

        # Should print warning for non-ESP device
        warning_printed = any(
            "does not use an ESP82xx" in str(call) for call in mock_print.call_args_list
        )
        assert warning_printed

    def test_no_warning_without_typo_field(self):
        """Test no warning when neither 'ability' nor 'ablilty' present."""
        protocol = tuya_discovery.TuyaDiscovery()

        # Device without ability/ablilty field
        device_data = {"ip": "10.42.42.42", "gwId": "unknowndevice"}
        device_info = json.dumps(device_data)
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + device_info.encode() + footer
        addr = ("10.42.42.42", 6666)

        with patch("builtins.print") as mock_print:
            protocol.datagram_received(data, addr)

        # Should NOT print warning
        warning_printed = any(
            "does not use an ESP82xx" in str(call) for call in mock_print.call_args_list
        )
        assert not warning_printed


class TestJSONParsingErrors:
    """Test handling of malformed JSON in broadcasts."""

    def setup_method(self):
        """Reset devices_seen set before each test."""
        tuya_discovery.devices_seen.clear()

    def test_handles_invalid_json_gracefully(self):
        """Test that invalid JSON doesn't crash the protocol."""
        protocol = tuya_discovery.TuyaDiscovery()

        # Create invalid JSON data
        invalid_json = "not valid json {"
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + invalid_json.encode() + footer
        addr = ("10.42.42.42", 6666)

        with patch("builtins.print"):
            # Should not raise exception
            protocol.datagram_received(data, addr)

        # Should still add to seen devices
        assert data in tuya_discovery.devices_seen

    def test_handles_empty_json_payload(self):
        """Test handling of empty JSON payload."""
        protocol = tuya_discovery.TuyaDiscovery()

        # Create empty payload
        header = b"\x00" * 20
        footer = b"\x00" * 8
        data = header + b"" + footer
        addr = ("10.42.42.42", 6666)

        with patch("builtins.print"):
            # Should not raise exception
            protocol.datagram_received(data, addr)


class TestMainFunction:
    """Test main() function setup."""

    def test_main_creates_event_loop(self):
        """Test that main() creates asyncio event loop."""
        with patch("asyncio.get_event_loop") as mock_get_loop:
            mock_loop = Mock()
            mock_get_loop.return_value = mock_loop
            mock_loop.create_datagram_endpoint.return_value = asyncio.Future()
            mock_loop.create_datagram_endpoint.return_value.set_result((None, None))

            with patch("builtins.print"):
                try:
                    # Start main in separate thread to avoid blocking
                    import threading

                    def run_main():
                        try:
                            tuya_discovery.main()
                        except KeyboardInterrupt:
                            pass

                    thread = threading.Thread(target=run_main, daemon=True)
                    thread.start()
                    thread.join(timeout=0.5)
                except:
                    pass

            # Verify event loop was accessed
            assert mock_get_loop.called

    def test_main_listens_on_port_6666(self):
        """Test that main() creates listener on port 6666."""
        with patch("asyncio.get_event_loop") as mock_get_loop:
            mock_loop = Mock()
            mock_get_loop.return_value = mock_loop

            # Mock datagram endpoint creation
            future = asyncio.Future()
            future.set_result((None, None))
            mock_loop.create_datagram_endpoint.return_value = future
            mock_loop.run_until_complete.return_value = (None, None)

            # Mock run_forever to raise KeyboardInterrupt immediately
            mock_loop.run_forever.side_effect = KeyboardInterrupt

            with patch("builtins.print"):
                try:
                    tuya_discovery.main()
                except KeyboardInterrupt:
                    pass

            # Check that endpoint was created with correct port
            calls = mock_loop.create_datagram_endpoint.call_args_list
            assert len(calls) >= 1
            # First call should be for port 6666
            assert calls[0][1]["local_addr"] == ("0.0.0.0", 6666)

    def test_main_listens_on_port_6667(self):
        """Test that main() creates encrypted listener on port 6667."""
        with patch("asyncio.get_event_loop") as mock_get_loop:
            mock_loop = Mock()
            mock_get_loop.return_value = mock_loop

            # Mock datagram endpoint creation
            future = asyncio.Future()
            future.set_result((None, None))
            mock_loop.create_datagram_endpoint.return_value = future
            mock_loop.run_until_complete.return_value = (None, None)

            # Mock run_forever to raise KeyboardInterrupt immediately
            mock_loop.run_forever.side_effect = KeyboardInterrupt

            with patch("builtins.print"):
                try:
                    tuya_discovery.main()
                except KeyboardInterrupt:
                    pass

            # Check that endpoint was created with correct port
            calls = mock_loop.create_datagram_endpoint.call_args_list
            assert len(calls) >= 2
            # Second call should be for port 6667
            assert calls[1][1]["local_addr"] == ("0.0.0.0", 6667)

    def test_main_handles_keyboard_interrupt(self):
        """Test that main() handles KeyboardInterrupt gracefully."""
        with patch("asyncio.get_event_loop") as mock_get_loop:
            mock_loop = Mock()
            mock_get_loop.return_value = mock_loop

            # Mock endpoint creation
            future = asyncio.Future()
            future.set_result((None, None))
            mock_loop.create_datagram_endpoint.return_value = future
            mock_loop.run_until_complete.return_value = (None, None)

            # Simulate KeyboardInterrupt
            mock_loop.run_forever.side_effect = KeyboardInterrupt

            with patch("builtins.print"):
                # Should not raise exception
                tuya_discovery.main()

            # Loop should be stopped
            assert mock_loop.stop.called


class TestDevicesSeenSet:
    """Test devices_seen global set."""

    def test_devices_seen_is_set(self):
        """Test that devices_seen is a set."""
        assert isinstance(tuya_discovery.devices_seen, set)

    def test_devices_seen_can_be_cleared(self):
        """Test that devices_seen set can be cleared."""
        tuya_discovery.devices_seen.add(b"test")
        assert len(tuya_discovery.devices_seen) > 0

        tuya_discovery.devices_seen.clear()
        assert len(tuya_discovery.devices_seen) == 0

    def test_duplicate_detection_works(self):
        """Test that duplicate device detection works correctly."""
        tuya_discovery.devices_seen.clear()

        test_data = b"test device data"
        assert test_data not in tuya_discovery.devices_seen

        tuya_discovery.devices_seen.add(test_data)
        assert test_data in tuya_discovery.devices_seen

        # Second add should not change set size
        size_before = len(tuya_discovery.devices_seen)
        tuya_discovery.devices_seen.add(test_data)
        assert len(tuya_discovery.devices_seen) == size_before


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
