from conans import ConanFile, AutoToolsBuildEnvironment, MSBuild, tools
import os
import shutil


class BreakpadConan(ConanFile):
    description = "Breakpad is a set of client and server components which implement a crash-reporting system."
    name = 'breakpad'
    version = '64'
    license = 'https://chromium.googlesource.com/breakpad/breakpad/+/master/LICENSE'
    url = 'https://gitlab.com/ArsenStudio/ArsenEngine/dependencies/conan-breakpad'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake'
    branch = 'master'
    exports = ["FindBREAKPAD.cmake", "patch/*"]

    def source(self):
        self.run(
            'git clone https://chromium.googlesource.com/breakpad/breakpad --branch %s --depth 1' % self.branch)
        if self.settings.os == 'Linux':
            self.run(
                'git clone https://chromium.googlesource.com/linux-syscall-support breakpad/src/third_party/lss')

    def build(self):
        if self.settings.os == 'Macos':
            arch = 'i386' if self.settings.arch == 'x86' else self.settings.arch
            self.run('xcodebuild -project breakpad/src/client/mac/Breakpad.xcodeproj -sdk macosx -target Breakpad ARCHS=%s ONLY_ACTIVE_ARCH=YES -configuration %s' %
                     (arch, self.settings.build_type))
        elif self.settings.os == 'Windows':
            tools.patch(patch_file="patch/common.gypi.patch", base_path="breakpad")
            self.run('gyp --no-circular-check -D win_release_RuntimeLibrary=2 -D win_debug_RuntimeLibrary=3 breakpad/src/client/windows/breakpad_client.gyp')
            msbuild = MSBuild(self)
            sln_filepath = "breakpad/src/client/windows/"

            msbuild.build(sln_filepath + "common.vcxproj")
            msbuild.build(sln_filepath + "handler/exception_handler.vcxproj")
            msbuild.build(sln_filepath + "crash_generation/crash_generation_client.vcxproj")
            msbuild.build(sln_filepath + "crash_generation/crash_generation_server.vcxproj")
            msbuild.build(sln_filepath + "sender/crash_report_sender.vcxproj")

        elif self.settings.os == 'Linux':
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure('breakpad/')
            env_build.make()

    def package(self):
        self.copy("FindBREAKPAD.cmake", ".", ".")
        self.copy('*.h', dst='include/common', src='breakpad/src/common')

        if self.settings.os == 'Macos':
            self.copy('*.h', dst='include/client/mac',
                      src='breakpad/src/client/mac')
            # self.copy doesn't preserve symbolic links
            shutil.copytree('breakpad/src/client/mac/build/%s/Breakpad.framework' % self.settings.build_type,
                            os.path.join(self.package_folder, 'lib', 'Breakpad.framework'), symlinks=True)
        elif self.settings.os == 'Windows':
            self.copy('*.h', dst='include/client/windows',
                      src='breakpad/src/client/windows')
            self.copy('*.h', dst='include/google_breakpad',
                      src='breakpad/src/google_breakpad')
            self.copy('*.lib', dst='lib', src='breakpad/src/client/windows/%s' %
                      self.settings.build_type, keep_path=False)
            self.copy('*.lib', dst='lib', src='breakpad/src/client/windows/handler/%s' %
                      self.settings.build_type, keep_path=False)
            self.copy('*.lib', dst='lib', src='breakpad/src/client/windows/crash_generation/%s' %
                      self.settings.build_type, keep_path=False)
            self.copy('*.lib', dst='lib', src='breakpad/src/client/windows/sender/%s' %
                      self.settings.build_type, keep_path=False)
            self.copy('*.exe', dst='bin',
                      src='breakpad/src/tools/windows/binaries')
        elif self.settings.os == 'Linux':
            self.copy("*.h", dst="include/client/linux",
                      src="breakpad/src/client/linux")
            self.copy("*.h", dst="include/google_breakpad/",
                      src="breakpad/src/google_breakpad")
            self.copy("*.h", dst="include/third_party/",
                      src="breakpad/src/third_party")
            self.copy("*.a", dst="lib", src="src/client/linux")
            self.copy("microdump_stackwalk", dst="bin", src="src/processor/")
            self.copy("minidump_dump", dst="bin", src="src/processor/")
            self.copy("minidump_stackwalk", dst="bin", src="src/processor/")
            self.copy("dump_syms", dst="bin", src="src/tools/linux/dump_syms/")
            self.copy("core2md", dst="bin", src="src/tools/linux/core2md/")
            self.copy("minidump-2-core", dst="bin",
                      src="src/tools/linux/md2core/")
            self.copy("minidump_upload", dst="bin",
                      src="src/tools/linux/symupload/")
            self.copy("sym_upload", dst="bin",
                      src="src/tools/linux/symupload/")

    def package_info(self):
        if self.settings.os == 'Windows':
            self.cpp_info.libs = ['breakpad']
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
