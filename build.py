#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default
import os

if __name__ == "__main__":
    remotes = []

    os.environ["CONAN_REMOTES"] = ",".join(remotes)
    os.environ["CONAN_BUILD_POLICY"] = "missing"

    builder = build_template_default.get_builder()

    builder.run()
