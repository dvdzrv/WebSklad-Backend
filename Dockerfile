FROM fedora/python
CMD ["dnf", "install", "fastfetch"]
CMD ["cd /home"]
CMD ["touch test.txt"]