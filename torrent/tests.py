from django.contrib.auth.models import User
from django.test import TestCase
from hashlib import sha1

from .models import Torrent

def get_sha1(name):
    return sha1(name.encode('utf-8')).hexdigest()

def create_dummy_torrent(torrent_name, status, owner):
    return Torrent.objects.create(
        name = torrent_name,
        hash = get_sha1(torrent_name),
        size = 0,
        peers = 0,
        status = status,
        progress = 0,
        download_rate = 0,
        downloaded_size = 0,
        owner = owner
    )


class TorrentTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user-1')
        self.user2 = User.objects.create(username='user-2')

    def test_torrent_create_and_get(self):
        torrent_name = "Test torrent 1"
        create_dummy_torrent(torrent_name, "queued", self.user1) 
        torrent = Torrent.objects.get(owner = self.user1)

        self.assertEqual(torrent.hash, get_sha1(torrent_name))

    def test_manager_copy_and_create(self):
        """
        Make sure that the Entry manager's `copy_and_create` method works
        """
        torrent_name = "Test torrent 2"
        create_dummy_torrent(torrent_name, "finished", self.user1) 

        exist_torrent = Torrent.objects.filter(
            hash = get_sha1(torrent_name),
            status = "finished"
        ).first()

        # Copy exist torrent and create new one for user2
        new_torrent = Torrent.objects.copy_and_create(exist_torrent, self.user2)
         
        self.assertEqual(exist_torrent.hash, new_torrent.hash)
        self.assertNotEqual(exist_torrent.owner, new_torrent.owner)

