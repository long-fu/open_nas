
## 磁盘挂载

```sh

lsblk

sudo blkid /dev/sdb1

# 输出
/dev/sdb1: UUID="f3671fdd-8306-4a24-ac34-ba779aaf0ed9" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="b1ea3025-7336-40bf-a506-79007d31889c"
/dev/sdb1: UUID="f3671fdd-8306-4a24-ac34-ba779aaf0ed9" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="b1ea3025-7336-40bf-a506-79007d31889c"

# 格式化磁盘
# sudo mkfs.ext4 /dev/sdb1

sudo vi /etc/fstab
# add ee5b3974-b0c2-4c1e-96fb-cbd2158284de 
# 手动更改 用户组
# UUID=0a26f12c-b971-495a-a010-558cacd7597d /home/haoshuai/data ext4 defaults,uid=1000,gid=1000 0 2
UUID=0a26f12c-b971-495a-a010-558cacd7597d /home/haoshuai/data ext4 defaults  0 2
```