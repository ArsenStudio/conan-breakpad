from conans import ConanFile, AutoToolsBuildEnvironment, MSBuild, tools
from utils import SourceDownloader, GitRepository
import os
import shutil


class BreakpadConan(ConanFile):
    name = "breakpad"
    version = "20181304"
    description = "Breakpad is a set of client and server components which implement a crash-reporting system."
    url = "https://gitlab.com/ArsenStudio/ArsenEngine/dependencies/conan-{0}".format(name)
    homepage = "https://chromium.googlesource.com/breakpad/breakpad/"

    # Breakpad License
    license = "BSD-3-Clause"

    exports = ["LICENSE.md", "utils/*", "FindBREAKPAD.cmake", "patch/*"]

    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        "shared": [True, False]
    }
    default_options = "shared=False"
    short_paths = True

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    commit = "9eac2058b70615519b2c4d8c6bdbfca1bd079e39"

    def source(self):
        srcdl = SourceDownloader(self)
        srcdl.addRepository(GitRepository(self, "https://chromium.googlesource.com/breakpad/breakpad",
                                          commit=self.commit))
        srcdl.get(self.source_subfolder)

        if self.settings.os == 'Linux':
            srcdl = SourceDownloader(self)
            srcdl.addRepository(GitRepository(self, "https://chromium.googlesource.com/linux-syscall-support",
                                              commit="a89bf7903f3169e6bc7b8efc10a73a7571de21cf"))
            srcdl.get(os.path.join(self.source_subfolder, "src/third_party/lss"))

    def build(self):
        absolute_source_subfolder = os.path.abspath(self.source_subfolder)
        tools.mkdir(self.build_subfolder)
        with tools.chdir(self.build_subfolder):

            if self.settings.os == 'Macos':
                arch = 'i386' if self.settings.arch == 'x86' else self.settings.arch
                self.run(("xcodebuild -project {source_folder}/src/client/mac/Breakpad.xcodeproj -sdk macosx" +
                         " -target Breakpad ARCHS={archs} ONLY_ACTIVE_ARCH=YES -configuration {config}")
                         .format(source_folder=absolute_source_subfolder, archs=arch, config=self.settings.build_type))
            elif self.settings.compiler == 'Visual Studio':
                tools.patch(patch_file="../patch/common.gypi.patch", base_path=absolute_source_subfolder)
                self.run("gyp --no-circular-check -D win_release_RuntimeLibrary=2 -D win_debug_RuntimeLibrary=3 " +
                         "{source_folder}/src/client/windows/breakpad_client.gyp"
                         .format(source_folder=absolute_source_subfolder))

                msbuild = MSBuild(self)
                sln_filepath = os.path.join(absolute_source_subfolder, "src/client/windows/")

                msbuild.build(sln_filepath + "common.vcxproj")
                msbuild.build(sln_filepath + "handler/exception_handler.vcxproj")
                msbuild.build(sln_filepath + "crash_generation/crash_generation_client.vcxproj")
                msbuild.build(sln_filepath + "crash_generation/crash_generation_server.vcxproj")
                msbuild.build(sln_filepath + "sender/crash_report_sender.vcxproj")

            elif self.settings.os == 'Linux' or (self.settings.os == 'Windows' and self.settings.compiler == 'gcc'):
                env_build = AutoToolsBuildEnvironment(self)
                env_build.configure(absolute_source_subfolder)
                env_build.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        self.copy("FindBREAKPAD.cmake", ".", ".")
        self.copy('*.h', dst='include/common', src=self.source_subfolder + '/src/common')

        if self.settings.os == 'Macos':
            self.copy('*.h', dst='include/client/mac', src=self.source_subfolder + '/src/client/mac')

            # self.copy doesn't preserve symbolic links
            shutil.copytree(self.source_subfolder + '/src/client/mac/build/{0}/Breakpad.framework'
                            .format(self.settings.build_type),
                            os.path.join(self.package_folder, 'lib', 'Breakpad.framework'), symlinks=True)
        elif self.settings.os == 'Windows':
            self.copy('*.h', dst='include/client/windows', src=self.source_subfolder + '/src/client/windows')
            self.copy('*.h', dst='include/google_breakpad', src=self.source_subfolder + '/src/google_breakpad')
            self.copy('*.lib', dst='lib', src=self.source_subfolder + '/src/client/windows/' + str(self.settings.build_type),
                      keep_path=False)
            self.copy('*.lib', dst='lib',
                      src=self.source_subfolder + '/src/client/windows/handler/' + str(self.settings.build_type),
                      keep_path=False)
            self.copy('*.lib', dst='lib',
                      src=self.source_subfolder + '/src/client/windows/crash_generation/' + str(self.settings.build_type),
                      keep_path=False)
            self.copy('*.lib', dst='lib',
                      src=self.source_subfolder + '/src/client/windows/sender/' + str(self.settings.build_type),
                      keep_path=False)
            self.copy('*.exe', dst='bin', src=self.source_subfolder + '/src/tools/windows/binaries')
        elif self.settings.os == 'Linux':
            self.copy("*.h", dst="include/client/linux", src=self.source_subfolder + "/src/client/linux")
            self.copy("*.h", dst="include/google_breakpad/", src=self.source_subfolder + "/src/google_breakpad")
            self.copy("*.h", dst="include/third_party/", src=self.source_subfolder + "/src/third_party")
            self.copy("*.a", dst="lib", src="src/client/linux")
            self.copy("microdump_stackwalk", dst="bin", src="src/processor/")
            self.copy("minidump_dump", dst="bin", src="src/processor/")
            self.copy("minidump_stackwalk", dst="bin", src="src/processor/")
            self.copy("dump_syms", dst="bin", src="src/tools/linux/dump_syms/")
            self.copy("core2md", dst="bin", src="src/tools/linux/core2md/")
            self.copy("minidump-2-core", dst="bin", src="src/tools/linux/md2core/")
            self.copy("minidump_upload", dst="bin", src="src/tools/linux/symupload/")
            self.copy("sym_upload", dst="bin", src="src/tools/linux/symupload/")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
