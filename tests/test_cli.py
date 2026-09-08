import contextlib
import importlib.machinery
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

app = importlib.machinery.SourceFileLoader('trump_watch', str(Path(__file__).resolve().parents[1]/'trump-watch')).load_module()


def fixture(approve='0.4', population=app.POPULATION, missing=False):
    b = io.BytesIO()
    ns = app.NS['m']
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr('xl/workbook.xml', '<workbook xmlns="%s" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="%s" r:id="x"/></sheets></workbook>' % (ns,population))
        z.writestr('xl/_rels/workbook.xml.rels','<Relationships><Relationship Id="x" Target="worksheets/sheet1.xml"/></Relationships>')
        rows=[]
        for i,(a,v) in enumerate([(app.QUESTION,'2025-01-28'),('Approve',approve),('Disapprove','0.58'),('Not sure','0.02'),('Unweighted base','1234'),('Base','1200')],1):
            rows.append('<row><c r="A%d" t="inlineStr"><is><t>%s</t></is></c>%s</row>'%(i,a,'' if missing and i==2 else '<c r="B%d"><v>%s</v></c>'%(i,v)))
        z.writestr('xl/worksheets/sheet1.xml','<worksheet xmlns="%s"><sheetData>%s</sheetData></worksheet>'%(ns,''.join(rows)))
    return b.getvalue()


class Tests(unittest.TestCase):
    def test_published_values(self):
        r=app.parse_workbook(fixture())[0]
        self.assertEqual((r['approve'],r['disapprove'],r['unweighted_base']),(40,58,1234))

    def test_rejects_bad_source(self):
        for b in [b'blocked',fixture('NaN'),fixture('2'),fixture(population='All adults'),fixture(missing=True)]:
            with self.subTest(), self.assertRaises((ValueError,zipfile.BadZipFile)):
                app.parse_workbook(b)

    def run_app(self,args):
        out=io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code=app.main(args)
        return code,out.getvalue()

    def test_cache_failure_and_offline(self):
        with tempfile.TemporaryDirectory() as d:
            args=['--cache-dir',d,'--json']
            with patch.object(app,'fetch',return_value=fixture()):
                code,out=self.run_app(args)
            self.assertEqual(code,0)
            self.assertTrue(json.loads(out)['stale'])
            before=(Path(d)/'polls.xlsx').read_bytes()
            with patch.object(app,'fetch',side_effect=OSError('network down')):
                code,out=self.run_app(args)
            self.assertEqual(code,2)
            self.assertIn('cached fallback',json.loads(out)['status'])
            self.assertEqual(before,(Path(d)/'polls.xlsx').read_bytes())
            with patch.object(app,'fetch',side_effect=AssertionError('must not fetch')):
                self.assertEqual(self.run_app(args+['--offline'])[0],0)

    def test_no_cache(self):
        with tempfile.TemporaryDirectory() as d, patch.object(app,'fetch',side_effect=OSError('down')):
            self.assertEqual(self.run_app(['--cache-dir',d])[0],1)
            self.assertEqual(self.run_app(['--cache-dir',d,'--offline'])[0],1)

    def test_corrupt_cache(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'polls.xlsx').write_bytes(b'bad')
            self.assertEqual(self.run_app(['--cache-dir',d,'--offline'])[0],1)

if __name__=='__main__': unittest.main()
