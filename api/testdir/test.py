import shutil

shutil.make_archive("/home/leap/Projects/TorrentBOX/api/testdir/iamdir"
, "zip",
 "/home/leap/Projects/TorrentBOX/api/testdir/iamdir")

shutil.rmtree("/home/leap/Projects/TorrentBOX/api/testdir/iamdir")
