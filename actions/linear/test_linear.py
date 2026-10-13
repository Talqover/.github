import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

sys.path.insert(0, os.path.dirname(__file__))
import linear  # noqa: E402

ISSUE = {"id": "uuid", "identifier": "DTECH-13", "url": "u"}


class ExtractTest(unittest.TestCase):
    def testBranchAcceptsLowercaseLinearSlug(self):
        self.assertEqual(linear.extract("matheus/dtech-13-convencao", branch=True), ["DTECH-13"])

    def testSlugsThatLookLikeIdsAreIgnored(self):
        self.assertEqual(linear.extract("fix/http-500-retry utf-8 phase-06", branch=True), [])

    def testProseOnlyCountsUppercaseAndDedupes(self):
        self.assertEqual(linear.extract("fixes TAL-1, tal-2 and TAL-1 again"), ["TAL-1"])


class UpsertTest(unittest.TestCase):
    def run_upsert(self, existing, prefix):
        calls = []

        def fake(query, variables):
            calls.append((query, variables))
            if query.startswith("query"):
                return {"data": {"issue": {"comments": {"nodes": existing}}}}
            if "commentUpdate" in query:
                return {"data": {"commentUpdate": {"success": True}}}
            return {"data": {"commentCreate": {"success": True}}}

        with mock.patch.object(linear, "gql", fake), redirect_stdout(io.StringIO()):
            linear.upsert(ISSUE, prefix + " new", prefix)
        return calls

    def testUpdatesTheCommentWithThePrefix(self):
        calls = self.run_upsert(
            [{"id": "c1", "body": "Claude review — PR #12: old"}], "Claude review — PR #12:"
        )
        self.assertIn("commentUpdate", calls[-1][0])
        self.assertEqual(calls[-1][1]["id"], "c1")

    def testPrOneDoesNotMatchPrTwelve(self):
        calls = self.run_upsert(
            [{"id": "c1", "body": "Claude review — PR #12: old"}], "Claude review — PR #1:"
        )
        self.assertIn("commentCreate", calls[-1][0])


class MainTest(unittest.TestCase):
    def testNoKeyWarnsAndExitsZero(self):
        with mock.patch.dict(os.environ, {}, clear=True), redirect_stderr(io.StringIO()) as err:
            self.assertEqual(linear.main(["comment", "TAL-1", "x"]), 0)
        self.assertIn("LINEAR_API_KEY is not set", err.getvalue())

    def testLinearOutageIsAWarningNotAFailure(self):
        def down(*_):
            raise linear.LinearUnavailable("HTTP 503")

        with mock.patch.dict(os.environ, {"LINEAR_API_KEY": "k"}), \
                mock.patch.object(linear, "gql", down), \
                redirect_stderr(io.StringIO()) as err:
            self.assertEqual(linear.main(["comment", "TAL-1", "x", "--replace-prefix", "p"]), 0)
        self.assertIn("Linear unavailable", err.getvalue())


if __name__ == "__main__":
    unittest.main()
