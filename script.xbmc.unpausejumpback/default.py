# -*- coding: utf-8 -*-
'''
Boblight for XBMC
Copyright (C) 2012 Team XBMC

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import xbmc
import xbmcaddon
import xbmcgui
import os

__addon__ = xbmcaddon.Addon()
__cwd__ = __addon__.getAddonInfo('path')
__scriptname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__icon__ = __addon__.getAddonInfo('icon')
__ID__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString

__profile__ = xbmc.translatePath( __addon__.getAddonInfo('profile') )
__resource__ = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )

sys.path.append (__resource__)

global g_jumpBackSecs
g_jumpBackSecs = 0

def log(msg):
  xbmc.log("### [%s] - %s" % (__scriptname__,msg,),level=xbmc.LOGDEBUG )

log( "[%s] - Version: %s Started" % (__scriptname__,__version__))

def loadSettings():
  global g_jumpBackSecs
  g_jumpBackSecs = int(float(__addon__.getSetting("jumpbacksecs")))

class MyPlayer( xbmc.Player ):
  def __init__( self, *args, **kwargs ):
    xbmc.Player.__init__( self )
    log('MyPlayer - init')
  
  def onPlayBackResumed( self ):
    global g_jumpBackSecs
    if g_jumpBackSecs != 0 and xbmc.Player().isPlayingVideo() and xbmc.Player().getTime() > g_jumpBackSecs:
      resumeTime = xbmc.Player().getTime() - g_jumpBackSecs
      xbmc.Player().seekTime(resumeTime)
      log( 'resumed with %ds jumpback' % g_jumpBackSecs )

class MyMonitor( xbmc.Monitor ):
  def __init__( self, *args, **kwargs ):
    xbmc.Monitor.__init__( self )
    log('MyMonitor - init')
        
  def onSettingsChanged( self ):
    loadSettings()

loadSettings()
xbmc_monitor = MyMonitor()
player_monitor = MyPlayer()
while not xbmc.abortRequested:
      xbmc.sleep(100)
