import unittest

import mock
from common import ssh_utility


class FakeChannelFile(object):
    def __init__(self, lines, channel=None):
        self.buf = iter(lines)
        self.channel = channel

    def __iter__(self):
        return self.buf


class TestSShClient(unittest.TestCase):
    """
    Creating a fake SSH connection and executing dummy command.
     And checking the functionality
    """

    @mock.patch.object(ssh_utility.paramiko.RSAKey, 'from_private_key')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    def test_init_rsa(self, mock_conn, mock_set, mock_rsa):
        ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath='dummy', keyfiletype='RSA', port=22, timeout=10)
        mock_conn.assert_called_with('ip', 22, 'user', mock_rsa.return_value)

    @mock.patch.object(ssh_utility.paramiko.DSSKey, 'from_private_key_file')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    def test_init_dsa(self, mock_conn, mock_set, mock_dss):
        ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath='dummy', keyfiletype='DSA', port=22, timeout=10)
        mock_conn.assert_called_with('ip', 22, 'user', mock_dss.return_value)

    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    def test_init(self, mock_conn, mock_set):
        ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath=None, keyfiletype=None, port=22, timeout=10)
        mock_conn.assert_called_with('ip', 22, 'user', 'pwd')

    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    def test_init_negative(self, mock_set):
        with self.assertRaises(Exception) as context:
            ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath=None, keyfiletype=None, port=22, timeout=10)
            self.assertTrue('Connection timeout' in str(context.exception))

    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'exec_command')
    def test_ssh(self, mock_exec, mock_conn, mock_set):
        mock_channel = mock.Mock()
        mock_exec.return_value = (FakeChannelFile(['input']),
                                  FakeChannelFile(['out_line1', 'out_line2'], mock_channel),
                                  FakeChannelFile(['err_line1', 'err_line2']))
        mock_channel.recv_exit_status.return_value = 0

        client = ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath=None,
                                     keyfiletype=None, port=22, timeout=10)
        return_data = client.execute_command('fake_command')

        mock_exec.assert_called()
        mock_channel.recv_exit_status.assert_called_with()
        self.assertEqual(return_data['status'], True)

    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'exec_command')
    def test_ssh_channel_negative(self, mock_exec, mock_conn, mock_set):
        mock_channel = mock.Mock()
        mock_exec.return_value = (FakeChannelFile(['input']),
                                  FakeChannelFile(['info'], mock_channel),
                                  FakeChannelFile(['err']))
        mock_channel.recv_exit_status.return_value = -1

        client = ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath=None,
                                     keyfiletype=None, port=22, timeout=10)
        return_data = client.execute_command('fake_command')

        mock_exec.assert_called()
        mock_channel.recv_exit_status.assert_called_with()
        self.assertEqual(return_data['status'], False)

    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    def test_ssh_channel_exception(self, mock_conn, mock_set):
        with self.assertRaises(Exception) as context:
            mock_channel = mock.Mock()
            mock_channel.recv_exit_status.return_value = 0

            client = ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath=None,
                                         keyfiletype=None, port=22, timeout=10)
            client.execute_command('fake_command')
            mock_channel.recv_exit_status.assert_called_with()
            self.assertTrue('Failed to execute the command!' in str(context.exception))

    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'open_sftp')
    def test_scp(self, mock_open, mock_conn, mock_set):
        mock_sftp = mock.Mock()
        mock_open.return_value = mock_sftp

        client = ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath=None,
                                     keyfiletype=None, port=22, timeout=10)
        return_data = client.upload_file('source_file', 'dest_file')

        mock_sftp.put.assert_called_with('source_file', 'dest_file')
        self.assertEqual(return_data['status'], True)

    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'set_missing_host_key_policy')
    @mock.patch.object(ssh_utility.paramiko.SSHClient, 'connect')
    def test_scp_negative(self, mock_conn, mock_set):
        with self.assertRaises(Exception) as context:
            mock_sftp = mock.Mock()

            client = ssh_utility.SSHUtil('ip', 'user', 'pwd', keyfilepath=None,
                                         keyfiletype=None, port=22, timeout=10)
            client.upload_file('source_file', 'dest_file')

            mock_sftp.put.assert_called_with('source_file', 'dest_file')
            self.assertTrue('Unable to upload the file to the remote server' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
