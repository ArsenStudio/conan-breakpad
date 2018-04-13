from conans import ConanFile, CMake
import os


class TestConan(ConanFile):
  settings = 'os', 'compiler', 'build_type', 'arch'
  generators = 'cmake'

  def build( self ):
    cmake = CMake(self)
    cmake.configure()
    cmake.build()

  def imports( self ):
    self.copy('*.dll', 'bin', 'bin')
    self.copy('*.dylib', 'bin', 'bin')

  def test( self ):
    os.chdir( 'bin' )
    self.run( '.%sexample' % os.sep )
