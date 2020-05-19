import paramiko
import sys
import hashlib
import os.path
import stat
import time

class FastTransport(paramiko.Transport):
    def __init__(self, sock):
        super(FastTransport, self).__init__(sock)
        #self.window_size = 2147483647
        self.window_size = 3 * 1024 * 1024
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)


class SSHBoxClient(object):
    def __init__(self, ip='', port=22, username='root', password=''):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        #self.t = paramiko.Transport((self.ip, self.port))
        self.t = FastTransport((self.ip, self.port))
        self.t.connect(username=self.username, password=self.password)
        self.t.use_compression()
        self.sftp = paramiko.SFTPClient.from_transport(self.t)
        
        # progress
        self.progress = 0
        
        # no block command
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.username, self.password)
    
    def _callback(self, a, b):
        #distance = int(a*100./int(b)) - self.progress
        #if distance > 1:
        #self.progress = int(a*100./int(b))
        sys.stdout.write('Data Transmission %10d [%3.2f%%]\r' %(a,a*100./int(b)))
        sys.stdout.flush()

    def get_all_files_in_remote_dir(self, remote_dir):
        # 保存所有文件的列表
        all_files = []

        # 去掉路径字符串最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        if remote_dir == '':
            remote_dir = '/'

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = self.sftp.listdir_attr(remote_dir)

        for x in files:
            # remote_dir目录中每一个文件或目录的完整路径
            if remote_dir == '/':
                remote_dir = ''

            filename = remote_dir + '/' + x.filename
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            # if stat.S_ISDIR(x.st_mode):
            #     all_files.extend(self.get_all_files_in_remote_dir(self.sftp, filename))
            # else:
            #     all_files.append(filename)
            file_item = {}
            file_item['name'] = x.filename
            file_item['path'] = filename
            file_item['size'] = x.st_size
            # 文件内容最后一次被修改的时间
            file_item['mTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x.st_mtime))

            if stat.S_ISDIR(x.st_mode):
                file_item['type'] = 'dir'
                all_files.append(file_item)
            else:
                file_item['type'] = 'file'
                all_files.append(file_item)
        return all_files

    def put(self, local_path='', remote_path=''):
        try:
            self.sftp.put(localpath=local_path, remotepath=remote_path, callback=self._callback)
        except Exception as e:
            print(str(e))
    
    def get(self, remote_path='', local_path=''):
        save_path = ''
        if local_path == '':
            pos = remote_path.rfind('/')
            save_path = remote_path[pos+1:]
        else:
            save_path = local_path
        print(save_path)
        
        if os.path.isfile(save_path):
            print(save_path+' is existed, delete it!')
            os.remove(save_path)
        
        print('Original file info:')
        print(self.exec_no_block('md5sum '+remote_path)[0])
        self.sftp.get(remote_path, save_path, self._callback)
        print('')
        print('Download file info:')
        print(self.get_md5(save_path), save_path)

    def get_file(self, remote_path='', local_path=''):
        pos = remote_path.rfind('/')
        local_filename = remote_path[pos:]
        if local_filename[0] != '/':
            local_filename = local_filename + '/'

        if local_path[-1] == '/':
            local_path = local_path[:-1]

        print(local_path+local_filename)
        self.get(remote_path, local_path+local_filename)
    
    def exec_no_block(self, cmd=''):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.readlines()
    
    def get_md5(self, local_path):
        hash_md5 = hashlib.md5()
        with open(local_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def rename(self, old_path, new_path):
        # print('rename:', old_path, new_path)
        self.sftp.rename(old_path, new_path)

    def remove(self, file_path):
        # print('remove:', file_path)
        if file_path == '/':
            return

        key_dirs = ['/bin', '/boot', '/dev', '/etc',
                    '/home', '/lib', '/opt', '/proc',
                    '/root', '/sbin', '/tmp', '/usr',
                    '/var']
        if file_path in key_dirs:
            return

        key_dirs = ['/bin/', '/boot/', '/dev/', '/etc/',
                    '/home/', '/lib/', '/opt/', '/proc/',
                    '/root/', '/sbin/', '/tmp/', '/usr/',
                    '/var/']
        if file_path in key_dirs:
            return

        self.ssh.exec_command('rm -rf "%s"' % (file_path))

    def copy(self, old_path, new_path):
        self.ssh.exec_command('cp -rf "%s" "%s"' % (old_path, new_path))

    def mkdir(self, dir_path):
        self.sftp.mkdir(dir_path)

    def get_history(self):
        rets = []
        _, stdout, _ = self.ssh.exec_command("cat ~/.bash_history")
        for item in stdout.readlines():
            if item[0] == '#':
                continue
            rets.append(item[:-1])
        return rets

    def get_df(self):
        rets = []
        _, stdout, _ = self.ssh.exec_command("df -lh")
        for item in stdout.readlines():
            if item[0] == '#':
                continue
            rets.append(item[:-1])
        return rets

    def close(self):
        self.t.close()
        self.ssh.close()



