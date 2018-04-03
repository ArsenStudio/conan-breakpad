from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(pure_c=False)
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["compiler"] == "clang":
            env_vars["CC"] = "clang"
            env_vars["CXX"] = "clang++"
    builder.run()
