import unittest
import tempfile
from pathlib import Path
import main

class OrganizerTests(unittest.TestCase):
    def test_categories(self):
        for name, group in [('A.JPG','Images'),('notes.pdf','Docs'),('audio.wav','Media'),('backup.tar.gz','Archives'),('app.tsx','Code'),('LICENSE','Others')]:
            self.assertEqual(main.category(name),group)
    def test_dry_plan_no_changes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'a.pdf').write_text('a');moves=main.plan(root)
            self.assertEqual(len(moves),1);self.assertTrue((root/'a.pdf').exists());self.assertFalse((root/'Docs').exists())
    def test_collision_keeps_existing(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'Docs').mkdir();(root/'Docs'/'a.pdf').write_text('old');(root/'a.pdf').write_text('new');moves=main.plan(root);main.apply(moves)
            self.assertEqual((root/'Docs'/'a.pdf').read_text(),'old');self.assertEqual((root/'Docs'/'a (1).pdf').read_text(),'new')
    def test_skip_symlinks_folders_hidden(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'folder').mkdir();(root/'.hidden').write_text('x');(root/'link').symlink_to(root/'folder');self.assertEqual(main.plan(root),[])
    def test_reject_destination_symlink(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as other:
            root=Path(d);(root/'Docs').symlink_to(other);(root/'a.pdf').write_text('x')
            with self.assertRaises(ValueError):main.plan(root)
    def test_race_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'a.txt').write_text('source');moves=main.plan(root);(root/'Docs').mkdir();moves[0][1].write_text('raced')
            with self.assertRaises(FileExistsError):main.apply(moves)
            self.assertEqual(moves[0][1].read_text(),'raced');self.assertEqual((root/'a.txt').read_text(),'source')
    def test_apply_and_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'x.zip').write_bytes(b'\x00\xff');main.apply(main.plan(root));self.assertEqual((root/'Archives'/'x.zip').read_bytes(),b'\x00\xff');self.assertFalse((root/'x.zip').exists())
    def test_destination_is_file(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'Images').write_text('x');(root/'photo.png').write_text('a')
            with self.assertRaises(ValueError):main.plan(root)

if __name__=='__main__':unittest.main()
