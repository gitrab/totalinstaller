# totalXBMC Installer based on original XBMCHUB.com Addon Installer  Module By: Blazetamer-2013-2014
# Refactored by: Yours Truly 2014!!

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time,xbmcvfs
import extract
import shutil
import subprocess
import datetime
import extract
import downloader
import popularpacks
import communitybuilds
import whufclee
import addonfix
import backuprestore

ADDON_ID   = 'plugin.program.totalinstaller'
BASEURL    = 'http://addons.totalxbmc.com/'
ADDON      = xbmcaddon.Addon(id=ADDON_ID)
HOME       = ADDON.getAddonInfo('path')
ARTPATH    = xbmc.translatePath(os.path.join(HOME, 'resources', 'art')) + os.sep
FANART     = os.path.join(ARTPATH, 'fanart.jpg')
zip        =  ADDON.getSetting('zip')
dialog     =  xbmcgui.Dialog()
dp         =  xbmcgui.DialogProgress()
USERDATA   =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS     =  xbmc.translatePath(os.path.join('special://home','addons'))
GUI        =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
FAVS       =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE     =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED   =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
RSS        =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS    =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB        =  xbmc.translatePath(os.path.join(zip))
skin       =  xbmc.getSkinDir()

#-----------------------------------------------------------------------------------------------------------------

def MAININDEX():
    addDir('Search For Addons','none','addonmenu', '', 'update.png')
#    addDir('Install Community Builds', 'none', 'community', '', 'categories2.png')
    addDir('Install Popular Packs', 'none', 'popular', '', 'categories2.png')
#    addDir('How To Guides', 'http://gdata.youtube.com/feeds/api/users/TotalXBMC/playlists?start-index=1&max-results=25', 'videoguides', 'Tutorial guides', 'categories2.png')
    addDir('Make Addons Gotham Compatible','none','gotham', '', 'update.png')
    addDir('Update My Addons (Force Refresh)', 'none', 'update', '', 'update.png')
    addDir('Backup My System', 'none', 'backup', '', 'update.png')
    addDir('Addon Fixes', 'none', 'addonfix', '', 'categories2.png')
    addDir('Upload Log','none','uploadlog', '', 'update.png')
    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def ADDONMENU():
    addDir('Manual Search','http://addons.totalxbmc.com/search/?keyword=','searchaddon', '', 'Search.png')
    if ADDON.getSetting('genre') == 'true':
        addDir('Search by Genres', 'none', 'genres', '', 'genres.png')

    if ADDON.getSetting('countries') == 'true':
        addDir('Search by Countries', 'none', 'countries', '', 'countries.png')

    if ADDON.getSetting('categories') == 'true':
        addDir('Search by XBMC Categories', 'none', 'categories', '', 'categories2.png')

    if ADDON.getSetting('repositories') == 'true':
        addDir('Install Repositories', 'category/repositories/', 'repolist', '', 'repositories.png')
    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------
def UPLOADLOG(): 
    if ADDON.getSetting('email')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("No Email Address Set", "A new window will Now open for you to enter your", "Email address. The logfile will be sent here")
        ADDON.openSettings()
    xbmc.executebuiltin('XBMC.RunScript(special://home/addons/plugin.program.totalinstaller/uploadLog.py)')

#-----------------------------------------------------------------------------------------------------------------

def INSTALLERROR(): 
    dialog = xbmcgui.Dialog()
    confirm = xbmcgui.Dialog().yesno('Upload A Log', 'If you\'ve received an error when attempting to install please upload a log and notify the forum at [COLOR=lime][B]www.totalxbmc.tv[/B][/COLOR] where the team can investigate the matter further.', 'Would you like to upload a log now?')
    if confirm == 0:
        return    
    elif confirm == 1:
		UPLOADLOG()

#-----------------------------------------------------------------------------------------------------------------

def PLAYVIDEO(url):
    import yt    
    yt.PlayVideo(url)

#-----------------------------------------------------------------------------------------------------------------
def VIDEOGUIDES(): 
    xbmc.executebuiltin('XBMC.RunAddon(plugin.video.whufclee)')

#-----------------------------------------------------------------------------------------------------------------
	
def addCategory(category, alt):    
    if ADDON.getSetting(alt) == 'true':
        addDir(category, 'category/categories2/%s/' % alt, 'addonlist', '', alt+'.png')   
 
def CATEGORIES():        
    addCategory('Audio Addons',  'audio')
    addCategory('Lyrics Addons', 'lyrics')

    if ADDON.getSetting('metadata') == 'true':
        addDir('Metadata', 'none', 'metadata', '', 'metadata.png')

    addCategory('Picture Addons', 'pictures')
    addCategory('Program Addons', 'programs')
    addCategory('Screensavers',   'screensaver')
    addCategory('Services',       'services')
    addCategory('Skins',          'skins')
    addCategory('Subtitles',      'subtitles')
    addCategory('Video Addons',   'video')
    addCategory('Weather',        'weather')
    addCategory('Web Interface',  'webinterface') 

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def addCountry(country, alt):
    if ADDON.getSetting(alt) == 'true':
        addDir(country, 'category/categories2/%s/' % alt, 'addonlist', '', alt+'.png')   

def AddPackCategory():        
    addCategory('Audio Addons',  'audio')
    addCategory('Lyrics Addons', 'lyrics')

    if ADDON.getSetting('metadata') == 'true':
        addDir('Metadata', 'none', 'metadata', '', 'metadata.png')

    addCategory('Picture Addons', 'pictures')
    addCategory('Program Addons', 'programs')
    addCategory('Screensavers',   'screensaver')
    addCategory('Services',       'services')
    addCategory('Skins',          'skins')
    addCategory('Subtitles',      'subtitles')
    addCategory('Video Addons',   'video')
    addCategory('Weather',        'weather')
    addCategory('Web Interface',  'webinterface') 

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------
def addMeta(meta, alt):    
    if ADDON.getSetting('meta'+alt) == 'true':
        addDir(meta, 'category/categories2/metadata/%s/' % alt, 'addonlist', '', alt+'.png')  


def METADATA():        
    addMeta('Album Metadata',       'albums')
    addMeta('Artist Metadata',      'artists')
    addMeta('Movie Metadata',       'movies')
    addMeta('Music Video Metadata', 'musicvideos')
    addMeta('TV Metadata',          'tvshows')

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def addGenre(genre):
    lower = genre.lower()
    lower = lower.replace(' ', '')

    #special cases
    lower = lower.replace('howto...',     'howto')
    lower = lower.replace('news&weather', 'news')
    lower = lower.replace('technology',   'tech')
    lower = lower.replace('tvshows',      'tv')
    lower = lower.replace('misc.',        'other')  
    lower = lower.replace('xxx',          'adult')

    if ADDON.getSetting(lower) == 'true':
        addDir(genre, 'category/genres/%s/' % lower, 'addonlist', '', lower+'.png')

def GENRES():       
    addGenre('Anime')
    addGenre('Audiobooks')
    addGenre('Comedy')
    addGenre('Comics')
    addGenre('Documentary')
    addGenre('Downloads')
    addGenre('Food')
    addGenre('Gaming')
    addGenre('Health')
    addGenre('How To...')
    addGenre('Kids')
    addGenre('Live TV')
    addGenre('Movies')
    addGenre('Music')
    addGenre('News & Weather')
    addGenre('Photos')
    addGenre('Podcasts')
    addGenre('Radio')
    addGenre('Religion')
    addGenre('Space')
    addGenre('Sports')
    addGenre('Technology')
    addGenre('Trailers')
    addGenre('TV Shows')
    addGenre('Misc.')
    addGenre('XXX')

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def addCountry(country):
    lower = country.lower()
    if ADDON.getSetting(lower) == 'true':
        addDir(country, 'category/countries/%s/' % lower, 'addonlist', '', lower+'.png')
    
def COUNTRIES():        
     #addCountry('African')
     addCountry('Arabic')
     addCountry('Asian')
     addCountry('Australian') 
     addCountry('Austrian')
     addCountry('Belgian')
     addCountry('Brazilian')
     addCountry('Canadian')
     addCountry('Chinese')
     addCountry('Columbian')
     addCountry('Czech')
     addCountry('Danish')
     addCountry('Dominican')
     addCountry('Dutch')
     addCountry('Egyptian')
     addCountry('Filipino')
     addCountry('Finnish')
     addCountry('French')
     addCountry('German')
     addCountry('Greek')
     addCountry('Hebrew')
     addCountry('Hungarian')
     addCountry('Icelandic')
     addCountry('Indian')
     addCountry('Irish')
     addCountry('Italian')
     addCountry('Japanese')
     addCountry('Korean')
     addCountry('Lebanese')
     addCountry('Mongolian')
     addCountry('Moroccan')
     addCountry('Nepali')
     addCountry('New Zealand')
     addCountry('Norwegian')
     addCountry('Pakistani')
     addCountry('Polish')
     addCountry('Portuguese')
     addCountry('Romanian')
     addCountry('Russian')
     addCountry('Singapore')
     addCountry('Spanish')
     addCountry('Swedish')
     addCountry('Swiss')
     addCountry('Syrian')
     addCountry('Tamil')
     addCountry('Thai')
     addCountry('Turkish')
     addCountry('UK')
     addCountry('USA')
     addCountry('Vietnamese')

     AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------

def nextPage(link, mode):
    nmatch = re.compile('"page last" href="(.+?)"><dfn title="next Page">').findall(link)
    if len(nmatch) > 0:
        addDir('Next Page', nmatch[0], mode, '', '')

#-----------------------------------------------------------------------------------------------------------------

def ADDONLIST(url):
    link  = OPEN_URL(url)
    match = re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" width="100%" alt="(.+?)"').findall(link)

    for url, image, name, in match:
        iconimage = BASEURL+ image
        add2HELPDir(name, url, 'addonindex', iconimage, FANART, '', 'addon')                    
        
    nextPage(link, 'addonlist')    

    AUTO_VIEW() 

#-----------------------------------------------------------------------------------------------------------------
    
def REPOLIST(url):
    d = xbmcgui.Dialog()
    d.ok('Repository Info', 'It\'s unlikely you\'ll need this section as the relevant repositories are installed when you install an addon. However if you encounter any issues you can install a repo and then try installing an addon via the traditional XBMC method.')
    link  = OPEN_URL(url)
    match = re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" width="100%" alt="(.+?)"').findall(link)

    for url, image, name, in match:
        iconimage = BASEURL + image
        add2HELPDir(name, url, 'addonindex', iconimage, FANART, '', 'addon')                    
        
    nextPage(link, 'addonlist')    

    AUTO_VIEW() 

#-----------------------------------------------------------------------------------------------------------------

def ADDONINDEX(name, url, filetype):
    link = OPEN_URL(url)

    videos = re.compile('https://www.youtube.com/watch\?v=(.+?)"target.+?alt="(.+?)" />').findall(link)
    match1 = re.compile('rel="nofollow">(.+?)</a>').findall(link)
#    match1 = re.compile('Repository:</strong>(.+?)<br />').findall(link)
    match2 = re.compile('<img src="(.+?)" alt=".+?" class="pic" /></span>').findall(link)
    match3 = re.compile('class="pic" /></span>\s*<h2>(.+?)</h2>').findall(link)
    match4 = re.compile('Repository:</strong> <a href="(.+?)"').findall(link)
    match5 = re.compile('Description:</h2><h4>(.+?)</h4>').findall(link)
    match6 = re.compile('Download:</strong><br /><a href="(.+?)"').findall(link)
    match7 = re.compile('Author:</strong> <a href=".+?">(.+?)</a>').findall(link)
    match8 = re.compile('Version:</strong>(.+?)<br').findall(link)
    match9 = re.compile('Add-on Type:</strong>(.+?)<br').findall(link)
    match10 = re.compile('Details:</strong>(.+?)</h1').findall(link)
    match11 = re.compile('Notes:</strong>(.+?)<br').findall(link)
    match12 = re.compile('Genres:</strong>(.+?)<br').findall(link)
    match13 = re.compile('Repository:</strong>(.+?)<br />').findall(link)
    match14 = re.compile('Platform:</strong>(.+?)<br />').findall(link)
    match15 = re.compile('Addon ID:</strong>(.+?)<br />').findall(link)

    repository1  = match1[0] if (len(match1) > 0) else ''
    image        = match2[0] if (len(match2) > 0) else ''
    name         = match3[0] if (len(match3) > 0) else ''
    repourl      = match4[0] if (len(match4) > 0) else 'none'
    description  = match5[0] if (len(match5) > 0) else 'Description not available at this time'
    addonurl     = match6[0] if (len(match6) > 0) else ''
    author       = match7[0] if (len(match7) > 0) else ''
    version      = match8[0] if (len(match8) > 0) else ''
    addontype    = match9[0] if (len(match9) > 0) else ''
    status       = match10[0] if (len(match10) > 0) else '[COLOR lime]No problems reported[/COLOR]'
    notes        = match11[0] if (len(match11) > 0) else 'None'
    genres       = match12[0] if (len(match12) > 0) else '[COLOR red]No genre information available, please help us categorise this correctly by posting on the forum at totalxbmc.tv[/COLOR]'
    repository2  = match13[0] if (len(match13) > 0) else ''
    platform     = match14[0] if (len(match14) > 0) else '[COLOR red]No platform information available[/COLOR]'
    addonid      = match15[0] if (len(match15) > 0) else ''
    iconimage    = BASEURL + image
	
#	check if there is a repo link, if not it needs use repository2 otherwise a load of garbage is added to the string
    if status == '[COLOR lime]No problems reported[/COLOR]':
        addDir('Live Info: '  +status, url, 'addonindex', '', 'categories2.png')
    else:
        addDir('Live Info: [COLOR=red]BROKEN - see notes below[/COLOR]', 'addonindex', '', 'categories2.png')

    addDir('Full Details (inc. any important notes)', url, 'addonstatus', '', 'categories2.png')
    addHELPDir('Install '+name, '  (Addon Type:'+addontype+')', addonurl, 'addoninstall', iconimage, FANART, description, 'addon', repourl, version)
    for video, name in videos:
        image = 'https://i1.ytimg.com/vi/%s/mqdefault.jpg' % video[:11]
        add2HELPDir(name, video, 'watch_video', image, fanart='', description='', filetype='', isFolder=False)
    addDir('[COLOR=red]Having problems installing?[/COLOR]','none','installerror', '', 'update.png')
    xbmcgui.Dialog().ok(name, 'This addon has been coded by [COLOR=blue] '+author+' [/COLOR]. Please consider showing your appreciation on the relevant support forum.')  

    AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------    
def ADDONSTATUS(url):
    link = OPEN_URL(url)

    videos = re.compile('https://www.youtube.com/watch\?v=(.+?)"target.+?alt="(.+?)" />').findall(link)
    match1 = re.compile('rel="nofollow">(.+?)</a>').findall(link)
#    match1 = re.compile('Repository:</strong>(.+?)<br />').findall(link)
    match2 = re.compile('<img src="(.+?)" alt=".+?" class="pic" /></span>').findall(link)
    match3 = re.compile('class="pic" /></span>\s*<h2>(.+?)</h2>').findall(link)
    match4 = re.compile('Repository:</strong> <a href="(.+?)"').findall(link)
    match5 = re.compile('Description:</h2><h4>(.+?)</h4>').findall(link)
    match6 = re.compile('Download:</strong><br /><a href="(.+?)"').findall(link)
    match7 = re.compile('Author:</strong> <a href=".+?">(.+?)</a>').findall(link)
    match8 = re.compile('Version:</strong>(.+?)<br').findall(link)
    match9 = re.compile('Add-on Type:</strong>(.+?)<br').findall(link)
    match10 = re.compile('Details:</strong>(.+?)</h1').findall(link)
    match11 = re.compile('Notes:</strong>(.+?)<br').findall(link)
    match12 = re.compile('Genres:</strong>(.+?)<br').findall(link)
    match13 = re.compile('Repository:</strong>(.+?)<br />').findall(link)
    match14 = re.compile('Platform:</strong>(.+?)<br />').findall(link)
    match15 = re.compile('Addon ID:</strong>(.+?)<br />').findall(link)

    repository1  = match1[0] if (len(match1) > 0) else ''
    image        = match2[0] if (len(match2) > 0) else ''
    name         = match3[0] if (len(match3) > 0) else ''
    repourl      = match4[0] if (len(match4) > 0) else 'none'
    description  = match5[0] if (len(match5) > 0) else 'Description not available at this time'
    addonurl     = match6[0] if (len(match6) > 0) else ''
    author       = match7[0] if (len(match7) > 0) else ''
    version      = match8[0] if (len(match8) > 0) else ''
    addontype    = match9[0] if (len(match9) > 0) else ''
    status       = match10[0] if (len(match10) > 0) else '[COLOR lime]No problems reported[/COLOR]'
    notes        = match11[0] if (len(match11) > 0) else 'None'
    genres       = match12[0] if (len(match12) > 0) else '[COLOR red]No genre information available, please help us categorise this correctly by posting on the forum at totalxbmc.tv[/COLOR]'
    repository2  = match13[0] if (len(match13) > 0) else ''
    platform     = match14[0] if (len(match14) > 0) else '[COLOR red]No platform information available[/COLOR]'
    addonid      = match15[0] if (len(match15) > 0) else ''
    iconimage    = BASEURL + image

    if len(repository1) < 50:
		TextBoxes(name+'   v.'+version, '[COLOR blue]Remember we rely on[/COLOR] [COLOR white]YOU[/COLOR] [COLOR blue]the brilliant XBMC/Kodi Community to keep this info updated.''\nIf any of this information is incorrect please let us know,''\n''just post a report on the forum at[/COLOR] [COLOR lime]www.totalxbmc.tv[/COLOR]\n\n\n''Supported Platforms:  '+platform+'\n\n''Addon Type:  '+addontype+'\n\n''Genre:  '+genres+'\n\n''Developer:  '+author+'\n\n''Repository:  '+repository1+'\n\n''Status:  [COLOR red]'+status+'[/COLOR]\n\n''Notes:  [COLOR yellow]'+notes+'[/COLOR]\n\n''Description:  [COLOR blue]'+description+'[/COLOR]')
    else:
		TextBoxes(name+'   v.'+version, '[COLOR blue]Remember we rely on[/COLOR] [COLOR white]YOU[/COLOR] [COLOR blue]the brilliant XBMC/Kodi Community to keep this info updated.''\nIf any of this information is incorrect please let us know,''\n''just post a report on the forum at[/COLOR] [COLOR lime]www.totalxbmc.tv[/COLOR]\n\n\n''Supported Platforms:  '+platform+'\n\n''Addon Type:  '+addontype+'\n\n''Genre:  '+genres+'\n\n''Developer:  '+author+'\n\n''Repository:  '+repository2+'\n\n''Status:  [COLOR red]'+status+'[/COLOR]\n\n''Notes:  [COLOR yellow]'+notes+'[/COLOR]\n\n''Description:  [COLOR blue]'+description+'[/COLOR]')
	
def TextBoxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(anounce); text=f.read()
      except: text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()  
#-----------------------------------------------------------------------------------------------------------------    

def SEARCHADDON(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Search add-ons" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	ADDONLIST(searchUrl)

	AUTO_VIEW()

#-----------------------------------------------------------------------------------------------------------------    

def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default
#-----------------------------------------------------------------------------------------------------------------    
  
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')    

#-----------------------------------------------------------------------------------------------------------------

def TOTALINSTALL(name, url, description, filetype, repourl):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))

    dp   = xbmcgui.DialogProgress()
    dp.create("First Launch:","Creating Database ",'','Only Shown on First Launch')

    lib = os.path.join(path,name+'.zip')

    try:    os.remove(lib)
    except: pass

    downloader.download(url, lib, dp)

    if filetype == 'addon':
        addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))

    time.sleep(2)
    extract.all(lib, addonfolder, '')
    
#-----------------------------------------------------------------------------------------------------------------

def DEPENDINSTALL(name, url):
    files = url.split('/')

    dependname = files[-1:]
    dependname = str(dependname)
    dependname = dependname.replace('[','')
    dependname = dependname.replace(']','')
    dependname = dependname.replace('"','')
    dependname = dependname.replace('[','')
    dependname = dependname.replace("'",'')
    dependname = dependname.replace(".zip",'')

    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp   = xbmcgui.DialogProgress()
    dp.create('Configuring Requirements:', '', 'Downloading and ', 'Installing '+ name)

    lib = os.path.join(path,name+'.zip')
    try:    os.remove(lib)
    except: pass

    downloader.download(url, lib, dp)

    addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))

    time.sleep(2)
    extract.all(lib, addonfolder, '')
        
    depends = xbmc.translatePath(os.path.join('special://home/addons/'+dependname,'addon.xml'))    
    source  = open( depends, mode = 'r' )
    link    = source.read( )
    source.close ( )

    dmatch = re.compile('import addon="(.+?)"').findall(link)
    for requires in dmatch:
        if not 'xbmc.python' in requires:
            print 'Script Requires --- ' + requires
            dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
            if not os.path.exists(dependspath):
                DEPENDINSTALL(requires, 'http://raw.github.com/totalxbmc/modules/master/'+requires+'.zip')

#-----------------------------------------------------------------------------------------------------------------

def ADDONINSTALL(name, url, filetype, repourl, author):
    print 'Installing Url : ' + url

    confirm = xbmcgui.Dialog().yesno(name, '[COLOR=lime][B]TotalXBMC[/B][/COLOR] do not host any addons and have no affiliation with the developer(s), as such we take no responsibility for the content it provides. Please check the laws in your country before installing. Do you wish to install?')  
    if confirm == 0:
        return    

    path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))    

    dp = xbmcgui.DialogProgress()
    dp.create('Download Progress:', 'Downloading your selection', '', 'Please Wait')

    lib = os.path.join(path, name+'.zip')

    try:    os.remove(lib)
    except: pass

    downloader.download(url, lib, dp)

    newfile   = url.split('-')[0:-1]
    newfile   = str(newfile)

    addonname = newfile.split('/')[-1:]
    addonname = str(addonname)
    addonname = addonname.replace('[','')
    addonname = addonname.replace(']','')
    addonname = addonname.replace('"','')
    addonname = addonname.replace('[','')
    addonname = addonname.replace("'",'')

    if filetype == 'addon':
        addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
    elif filetype == 'media':
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
    elif filetype == 'main':
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))

    time.sleep(2)
    extract.all(lib, addonfolder, dp)

    try:
        #Start Addon Depend Search==================================================================
        depends = xbmc.translatePath(os.path.join('special://home/addons/'+addonname, 'addon.xml'))    
        source  = open(depends, mode = 'r')
        link    = source.read()
        source.close ()

        dmatch = re.compile('import addon="(.+?)"').findall(link)
        for requires in dmatch:
            if not 'xbmc.python' in requires:
                dependspath = xbmc.translatePath(os.path.join('special://home/addons', requires))
                if not os.path.exists(dependspath):
                    DEPENDINSTALL(requires, 'http://raw.github.com/totalxbmc/modules/master/'+requires+'.zip')
    except:
        pass            
        
    if  'none' not in repourl:
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
     
        dp = xbmcgui.DialogProgress()
        dp.create('Updating Repo if needed:', 'Configuring Installation', '', '')

        lib = os.path.join(path,name+'.zip')

        try:    os.remove(lib)
        except: pass

        downloader.download(repourl, lib, '')

        if filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
        elif filetype == 'media':
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
        elif filetype == 'main':
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))

        time.sleep(2)
        extract.all(lib, addonfolder, dp)
    xbmc.executebuiltin( 'UpdateAddonRepos' )            
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmcgui.Dialog().ok('Item installed successfully', 'If you like what we\'re creating at [COLOR=lime][B]totalxbmc.tv[/COLOR][/B] please come', 'and make yourself know on the forum. All donations are very', 'welcome and will go towards the running costs. Thank you!')
	
#-----------------------------------------------------------------------------------------------------------------

def UPDATEREPO():
#    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmc.executebuiltin( 'UpdateAddonRepos' )    
    xbmcgui.Dialog().ok('Force Refresh Started Successfully', 'Depending on the speed of your device it could take a few minutes for the update to take effect.','','[COLOR=blue]For all your XBMC/Kodi support visit[/COLOR] [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')

#-----------------------------------------------------------------------------------------------------------------

def AUTO_VIEW(content = ''):
    if not content:
        return

    xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') != 'true':
        return

    if content == 'addons':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting('addon_view'))
    else:
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting('default-view'))

#-----------------------------------------------------------------------------------------------------------------

def addDir(name, url, mode, description, iconimage = ''): 
    if len(iconimage) > 0:
        iconimage = ARTPATH + iconimage
    else:
        iconimage = 'DefaultFolder.png'

    if url != 'none':
        if not url.startswith(BASEURL):
            url = BASEURL + url

    u  = sys.argv[0]
    u += "?url="  + urllib.quote_plus(url)
    u += "&name=" + urllib.quote_plus(name)
    u += "&mode=" + str(mode)

    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)

    liz.setProperty("Fanart_Image", FANART )
    
    if mode==None or mode=='videoguides' or mode=='backup_option' or mode=='restore_zip' or url==None or len(url)<1:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)

	
#-----------------------------------------------------------------------------------------------------------------

def addHELPDir(name, addontype, url, mode, iconimage, fanart, description, filetype, repourl='', version='', author=''):
        u  = sys.argv[0]
        u += "?url="         + urllib.quote_plus(url)
        u += "&name="        + urllib.quote_plus(name)
        u += "&filetype="    + urllib.quote_plus(filetype)
        u += "&repourl="     + urllib.quote_plus(repourl)
        u += "&mode="        + str(mode)
                        
        liz = xbmcgui.ListItem(name+addontype, iconImage='DefaultFolder.png', thumbnailImage=iconimage)

        liz.setInfo(type="Video", infoLabels={ 'title': name, 'plot': description } )
        liz.setProperty('Fanart_Image', fanart )

        liz.setProperty('Addon.Description', description )
        liz.setProperty('Addon.Creator', author )
        liz.setProperty('Addon.Version', version )        

        addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)

#-----------------------------------------------------------------------------------------------------------------

def add2HELPDir(name, url, mode, iconimage, fanart, description, filetype, isFolder=True):
        u  = sys.argv[0]
        u += "?url="         + urllib.quote_plus(url)
        u += "&name="        + urllib.quote_plus(name)
        u += "&filetype="    + urllib.quote_plus(filetype)
        u += "&mode="        + str(mode)
        
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)

        liz.setInfo(type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty("Fanart_Image", fanart )

        addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

#-----------------------------------------------------------------------------------------------------------------  
# This will edit the addon.xml and insert the correct strings
def EDITMXL(addonid, name):
    path = xbmc.translatePath(os.path.join('special://home', 'addons'))

    import glob
    dp = xbmcgui.DialogProgress()
    dp.create("Installing Addon","Please wait whilst your addon is installed",'', '')
    for infile in glob.glob(os.path.join(path, addonid)):
     for file in glob.glob(os.path.join(infile, '*.*')):
             if 'addon.xml' in file:
                 dp.update(0,"Creating new addon.xml",file, 'Please Wait')
                 a=open(file).read()
                 b=a.replace('test', addonid).replace('testname', name)
                 f = open(file, mode='w')
                 f.write(str(b))
                 f.close()

    dialog = xbmcgui.Dialog()
    dialog.ok("Addon now installing", "Your addon is now being installed, please be patient whilst the system checks for any online updates to the addon. If you find the addon is broken or it has bugs please contact us on the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B] so the team can update the live info. Thank you.")             

#-----------------------------------------------------------------------------------------------------------------  
# Thanks to Mikey1234 for this code - taken from the xunity maintenance addon
def GOTHAMCONFIRM():
    dialog = xbmcgui.Dialog()
    confirm = xbmcgui.Dialog().yesno('Convert Addons To Gotham', 'This will edit your addon.xml files so they show as Gotham compatible. It\'s doubtful this will have any effect on whether or not they work but it will get rid of the annoying incompatible pop-up message. Do you wish to continue?')
    if confirm == 0:
        return    
    elif confirm == 1:
		GOTHAM()
		
def GOTHAM():
    path = xbmc.translatePath(os.path.join('special://home', 'addons'))

    import glob
    dp = xbmcgui.DialogProgress()
    dp.create("Gotham Addon Fix","Please wait whilst your addons",'', 'are being made Gotham compatible.')
    for infile in glob.glob(os.path.join(path, '*.*')):
     for file in glob.glob(os.path.join(infile, '*.*')):
             if 'addon.xml' in file:
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a=open(file).read()
                 b=a.replace('addon="xbmc.python" version="1.0"','addon="xbmc.python" version="2.1.0"').replace('addon="xbmc.python" version="2.0"','addon="xbmc.python" version="2.1.0"')
                 f = open(file, mode='w')
                 f.write(str(b))
                 f.close()

    dialog = xbmcgui.Dialog()
    dialog.ok("Your addons have now been made compatible", "If you still find you have addons that aren't working please run the addon so it throws up a script error, upload a log and post details on the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B] so the team can look into it. Thank you.")             

#-----------------------------------------------------------------------------------------------------------------  
def BACKUP_OPTION():
    addDir('[COLOR=lime][B]FULL BACKUP[/COLOR][/B]','url','backup','','Back Up Your Full System')
    addDir('Backup Just Your Addons','addons','backup_zip','','Back Up Your Addons')
    addDir('Backup Just Your Addon UserData','addon_data','backup_zip','','Back Up Your Addon Userdata')
    addDir('Backup Guisettings.xml',GUI,'restore_backup_xml','','Back Up Your guisettings.xml')
    if os.path.exists(FAVS):
        addDir('Backup Favourites.xml',FAVS,'restore_backup_xml','','Back Up Your favourites.xml')
    if os.path.exists(SOURCE):
        addDir('Backup Source.xml',SOURCE,'restore_backup_xml','','Back Up Your sources.xml')
    if os.path.exists(ADVANCED):
        addDir('Backup Advancedsettings.xml',ADVANCED,'restore_backup_xml','','Back Up Your advancedsettings.xml')
    if os.path.exists(KEYMAPS):
        addDir('Backup Advancedsettings.xml',KEYMAPS,'restore_backup_xml','','Back Up Your keyboard.xml')
    if os.path.exists(RSS):
        addDir('Backup RssFeeds.xml',RSS,'restore_backup_xml','','Back Up Your RssFeeds.xml')    
    if os.path.exists(os.path.join(USB,'backup.zip')):   
        addDir('[COLOR=orange][B]FULL RESTORE[/COLOR][/B]','url','restore_zip','','Back Up Your Full System')      
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        addDir('Restore Your Addons','addons','restore_zip','','Restore Your Addons')  
    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir('Restore Your Addon UserData','addon_data','restore_zip','','Restore Your Addon UserData')           
    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('Restore Guisettings.xml',GUI,'restore_backup_xml','','Restore Your guisettings.xml')
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('Restore Favourites.xml',FAVS,'restore_backup_xml','','Restore Your favourites.xml')
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('Restore Source.xml',SOURCE,'restore_backup_xml','','Restore Your sources.xml')
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('Restore Advancedsettings.xml',ADVANCED,'restore_backup_xml','','Restore Your advancedsettings.xml')        
    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('Restore Advancedsettings.xml',KEYMAPS,'restore_backup_xml','','Restore Your keyboard.xml')
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('Restore RssFeeds.xml',RSS,'restore_backup_xml','','Restore Your RssFeeds.xml')   
		
#-----------------------------------------------------------------------------------------------------------------
		
def addDirectoryItem(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder=True)
    
#-----------------------------------------------------------------------------------------------------------------
    
def get_params():    
    if len(sys.argv[2]) < 2:
        return []

    param = []

    params        = sys.argv[2]
    cleanedparams = params.replace('?','')

    if (params[len(params)-1] == '/'):
        params = params[0:len(params)-2]

    pairsofparams = cleanedparams.split('&')
    param         = {}

    for i in range(len(pairsofparams)):
        splitparams = {}
        splitparams = pairsofparams[i].split('=')

        if (len(splitparams)) == 2:
            param[splitparams[0]] = splitparams[1]

    return param

#-----------------------------------------------------------------------------------------------------------------

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
author=None

try:    mode = urllib.unquote_plus(params['mode'])
except: mode = None

try:    url = urllib.unquote_plus(params['url'])
except: url = ''

try:    name = urllib.unquote_plus(params['name'])
except: name = ''

try:    type = urllib.unquote_plus(params['filetype'])
except: type = ''

try:    repo = urllib.unquote_plus(params['repourl'])
except: repo = ''

try:    author = urllib.unquote_plus(params['repourl'])
except: author = 'anonymous'

try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

try:    description=urllib.unquote_plus(params["description"])
except: pass

#print "Mode : " + str(mode)
#print "URL  : " + str(url)
#print "Name : " + str(name)
#print "Repo : " + str(repo)
#print "Type : " + str(type)


if mode   == None                 : MAININDEX()
elif mode == 'categories'         : CATEGORIES()
elif mode == 'metadata'           : METADATA()
elif mode == 'genres'             : GENRES()
elif mode == 'countries'          : COUNTRIES()
elif mode == 'update'             : UPDATEREPO()
elif mode == 'addonlist'          : ADDONLIST(url)
elif mode == 'addonmenu'          : ADDONMENU()
elif mode == 'uploadlog'          : UPLOADLOG()
elif mode == 'repolist'           : REPOLIST(url)
elif mode == 'addonindex'         : ADDONINDEX(  name, url, type)
elif mode == 'addoninstall'       : ADDONINSTALL(name, url, type, repo, author)
elif mode == 'watch_video'        : PLAYVIDEO(url)
elif mode == 'runvids'            : UPDATEREPO()
elif mode == 'totalvids'          : TOTALVIDS(params)
elif mode == 'searchaddon'        : print""+url; SEARCHADDON(url)
elif mode == 'gotham'             : GOTHAMCONFIRM()
elif mode == 'showinfo'           : SHOWINFO(name, version, platform, addontype, genres, author, repository1, status, notes, description, repository2)
elif mode == 'popular'            : popularpacks.POPULAR()
elif mode == 'popularpacks'       : popularpacks.ADDONPACKMASTER()
elif mode == 'community'          : communitybuilds.COMMUNITY()
elif mode == 'addonstatus'        : ADDONSTATUS(url)
elif mode == 'videoguides'        : whufclee.main_list(url)
elif mode == 'installerror'       : INSTALLERROR()
elif mode == 'addonfix'           : addonfix.fixes()
elif mode == 'backupoptions'      : BACKUP_OPTION()
elif mode == 'backup'             : backuprestore.BACKUP()
elif mode == 'restore'            : backuprestore.RESTORE()    
elif mode == 'restore_backup_xml' : backuprestore.RESTORE_BACKUP_XML(name,url,description)
elif mode == 'restore_zip'        : backuprestore.RESTORE_ZIP_FILE(url)  

if 'repo' in name.lower() and len(repo) > 0:
    url = repo
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))