# Creating test filesystem
```sh
touch test.iso
sudo dd if=/dev/zero of=./test.iso bs=1024 count=1048576 status=progress
cfdisk test.iso
```

Then add a Linux Partition

```sh
sudo losetup -fP ./test.iso
sudo mkfs.btrfs /dev/loop0p1
sudo mkdir /mnt/test
sudo mount /dev/loop0p1 /mnt/test
```

Then start creating files like it's any other drive.

# Making the data dump

