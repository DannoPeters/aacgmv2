# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

import subprocess
import numpy as np
import os


def setup_function(function):
    try:
        os.remove('tests/output.txt')
    except:
        pass

teardown_function = setup_function


def test_module_invocation():
    p = subprocess.Popen(['python', '-m', 'aacgmv2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [[57.4761, 93.5572], [58.5332, 93.9607], [59.5852, 94.3897]], rtol=1e-4)


def test_convert_g2a():
    p = subprocess.Popen(['aacgmv2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [[57.4761, 93.5572], [58.5332, 93.9607], [59.5852, 94.3897]], rtol=1e-4)


def test_convert_a2g():
    p = subprocess.Popen(['aacgmv2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-v'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [[51.6547, -66.6601], [52.6725, -66.7555], [53.6914, -66.8552]], rtol=1e-4)


def test_convert_trace_g2a():
    p = subprocess.Popen(['aacgmv2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-t'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [[57.4736, 93.5676], [58.5305, 93.9716], [59.5825, 94.4009]], rtol=1e-4)


def test_convert_trace_a2g():
    p = subprocess.Popen(['aacgmv2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-t', '-v'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [[51.6454, -66.6444], [52.6671, -66.7432], [53.6899, -66.8469]], rtol=1e-4)


def test_convert_geocentric():
    p = subprocess.Popen(['aacgmv2', 'convert', '-i', 'tests/test_convert.txt', '-d', '20150224',
                          '-o', 'tests/output.txt', '-g'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [[57.6697, 93.6319], [58.7223, 94.0385], [59.7695, 94.4708]], rtol=1e-4)


def test_convert_today():
    p = subprocess.Popen(['aacgmv2', 'convert', '-i', 'tests/test_convert.txt'])
    p.communicate()
    p.wait()


def test_convert_single_line():
    p = subprocess.Popen(['aacgmv2', 'convert', '-i', 'tests/test_convert_single_line.txt',
                          '-d', '20150224', '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [57.4761, 93.5572], rtol=1e-4)


def test_convert_stdin_stdout():
    p = subprocess.Popen('echo 60 15 300 | aacgmv2 convert -d 20150224', shell=True, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    p.wait()
    assert b'57.47612194 93.55719875' in stdout


def test_convert_mlt_a2m():
    p = subprocess.Popen(['aacgmv2', 'convert_mlt', '-i', 'tests/test_convert_mlt.txt',
                          '20150224140015', '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [9.185806, 9.919139, 10.652473], rtol=1e-6)


def test_convert_mlt_m2a():
    p = subprocess.Popen(['aacgmv2', 'convert_mlt', '-i', 'tests/test_convert_mlt.txt',
                          '20150224140015', '-o', 'tests/output.txt', '-v'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [238.212909, 43.212909, 208.212909], rtol=1e-6)
    import shutil
    shutil.copyfile('tests/output.txt', 'tests/asd.txt')


def test_convert_mlt_single_line():
    p = subprocess.Popen(['aacgmv2', 'convert_mlt', '-i', 'tests/test_convert_mlt_single_line.txt',
                          '20150224140015', '-o', 'tests/output.txt'])
    p.communicate()
    p.wait()
    data = np.loadtxt('tests/output.txt')
    np.testing.assert_allclose(data, [9.185806], rtol=1e-6)


def test_convert_mlt_stdin_stdout():
    p = subprocess.Popen('echo 12 | aacgmv2 convert_mlt -v 20150224140015', shell=True, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    p.wait()
    assert b'43.21290868' in stdout


def test_convert_mlt_stdin_stdout_order():
    p = subprocess.Popen('echo 12 | aacgmv2 convert_mlt 20150224140015 -v', shell=True, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()
    p.wait()
    assert b'43.21290868' in stdout
