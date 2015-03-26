import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import weblogin
import zipfile
import ntpath

ARTPATH      =  'http://totalxbmc.tv/totalrevolution/art/' + os.sep
FANART       =  'http://totalxbmc.tv/totalrevolution/art/fanart.jpg'
ADDON        =  xbmcaddon.Addon(id='plugin.program.community.builds')
AddonID      =  'plugin.program.community.builds'
AddonTitle   =  "[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]"
zip          =  ADDON.getSetting('zip')
localcopy    =  ADDON.getSetting('localcopy')
keyid        =  ADDON.getSetting('keyid')
privatebuilds=  ADDON.getSetting('private')
privateuser  =  ADDON.getSetting('privateuser')
reseller     =  ADDON.getSetting('reseller')
resellername =  ADDON.getSetting('resellername')
resellerid   =  ADDON.getSetting('resellerid')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
HOME         =  xbmc.translatePath('special://home/')
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
DATABASE     =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
GUISETTINGS  =  os.path.join(USERDATA,'guisettings.xml')
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX       =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
CBPATH       =  xbmc.translatePath(os.path.join(USB,'Community Builds',''))
cookiepath   =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'cookiejar'))
startuppath  =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'startup.xml'))
tempfile     =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'temp.xml'))
idfile       =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'id.xml'))
idfiletemp   =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'idtemp.xml'))
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()
EXCLUDES     =  ['plugin.program.community.builds']
username     =  ADDON.getSetting('username')
password     =  ADDON.getSetting('password')
login        =  ADDON.getSetting('login')
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
GUINEW       =  xbmc.translatePath(os.path.join(userdatafolder,'guinew.xml'))
guitemp      =  xbmc.translatePath(os.path.join(userdatafolder,'guitemp',''))
factory      =  xbmc.translatePath(os.path.join(HOME,'..','factory','_DO_NOT_DELETE.txt'))
tempdbpath   =  xbmc.translatePath(os.path.join(USB,'Database'))
urlbase      =  'None'
#-----------------------------------------------------------------------------------------------------------------    
#Simple shortcut to create a notification
def Notify(title,message,times,icon):
    icon = notifyart+icon
    print "icon: "+str(icon)
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
#-----------------------------------------------------------------------------------------------------------------    
#Popup class - thanks to whoever codes the help popup in TVAddons Maintenance for this section. Unfortunately there doesn't appear to be any author details in that code so unable to credit by name.
class SPLASH(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs): self.shut=kwargs['close_time']; xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)"); xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")
    def onFocus(self,controlID): pass
    def onClick(self,controlID): 
        if controlID==12: xbmc.Player().stop(); self._close_dialog()
    def onAction(self,action):
        if action in [5,6,7,9,10,92,117] or action.getButtonCode() in [275,257,261]: xbmc.Player().stop(); self._close_dialog()
    def _close_dialog(self):
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)"); time.sleep( .4 ); self.close()
#-----------------------------------------------------------------------------------------------------------------    
#Set popup xml based on platform
def pop():
    popup=SPLASH('totalxbmc.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34)
    popup.doModal()
    del popup
#-----------------------------------------------------------------------------------------------------------------    
#Initial online check for new video
def VideoCheck():
    print skin
    import yt
    unlocked = 'no'
    if not os.path.exists(userdatafolder):
        os.makedirs(userdatafolder)
    if not os.path.exists(startuppath):
        localfile = open(startuppath, mode='w+')
        localfile.write('date="01011001"\nversion="0.0"')
        localfile.close()
    if not os.path.exists(idfile):
        localfile = open(idfile, mode='w+')
        localfile.write('id="None"\nname="None"')
        localfile.close()
    BaseURL='http://totalxbmc.tv/totalrevolution/Community_Builds/update.txt'
    link = OPEN_URL(BaseURL).replace('\n','').replace('\r','')
    datecheckmatch = re.compile('date="(.+?)"').findall(link)
    videomatch = re.compile('video="https://www.youtube.com/watch\?v=(.+?)"').findall(link)
#    splashmatch = re.compile('splash="(.+?)"').findall(link)
#    splashmatch2 = re.compile('splash2="(.+?)"').findall(link)
    datecheck  = datecheckmatch[0] if (len(datecheckmatch) > 0) else ''
    videocheck  = videomatch[0] if (len(videomatch) > 0) else ''
#    splashcheck  = splashmatch[0] if (len(splashmatch) > 0) else ''
#    splashcheck2  = splashmatch2[0] if (len(splashmatch2) > 0) else ''

    localfile = open(startuppath, mode='r')
    content = file.read(localfile)
    file.close(localfile)
    localdatecheckmatch = re.compile('date="(.+?)"').findall(content)
    localdatecheck  = localdatecheckmatch[0] if (len(localdatecheckmatch) > 0) else ''
    localversionmatch = re.compile('version="(.+?)"').findall(content)
    localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
    localfile2 = open(idfile, mode='r')
    content2 = file.read(localfile2)
    file.close(localfile2)
    localidmatch = re.compile('id="(.+?)"').findall(content2)
    localidcheck  = localidmatch[0] if (len(localidmatch) > 0) else 'None'
    localbuildmatch = re.compile('name="(.+?)"').findall(content2)
    localbuildcheck  = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''
    print "localbuildmatch: "+str(localbuildmatch)
    print "localbuildcheck: "+str(localbuildcheck)
    # if localidcheck == "None":
        # if os.path.exists(INSTALL):
            # os.remove(INSTALL)
    if  int(localdatecheck) < int(datecheck):
        replacefile = content.replace(localdatecheck,datecheck)
        writefile = open(startuppath, mode='w')
        writefile.write(str(replacefile))
        writefile.close()
        yt.PlayVideo(videocheck, forcePlayer=True)
        xbmc.sleep(500)
        while xbmc.Player().isPlaying():
            xbmc.sleep(500)
    else:
        pass
    logged_in = weblogin.doLogin(cookiepath,username,password)
    if login == 'true':
        if logged_in == True:
            unlocked = 'yes'
            Notify('Login Successful', 'Welcome back '+username,'4000','tick.png')
        elif logged_in == False:
            dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','There is an error with your login information, please check','your username and password, remember this is case','sensitive so use capital letters where needed.')
            ADDON.openSettings(sys.argv[0])
    else:
        pop()
    CATEGORIES(localbuildcheck,localversioncheck,localidcheck,unlocked)
#-----------------------------------------------------------------------------------------------------------------    
#Function to create a text box
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
#---------------------------------------------------------------------------------------------------
#Create a community (universal) backup - this renames paths to special:// and removes unwanted folders
def COMMUNITY_BACKUP():  
    CHECK_DOWNLOAD_PATH()
    path = xbmc.translatePath(os.path.join(USB,'tempbackup'))
    fullbackuppath = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds',''))
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    if os.path.exists(path):
        shutil.rmtree(path)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    # if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0
    # we need to set the title to our query
    title = urllib.quote_plus(vq)
    choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'Do you want to include your addon_data folder?', 'This contains ALL addon settings including passwords.', 'We strongly recommend against this unless all data has been removed.', yeslabel='Yes',nolabel='No')
    if choice == 1:
        inc_data = ''
    elif choice == 0:
        inc_data = 'addon_data'
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]",'[COLOR=dodgerblue]Copying files to [/COLOR][COLOR=yellow]'+path+'[/COLOR]','If you have a slow device or large build this may', 'take a while so you may want to go and make a cuppa...')
    shutil.copytree(HOME, path, symlinks=False, ignore=shutil.ignore_patterns(inc_data,"cache","system","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Thumbnails","Textures13.db","peripheral_data","library","keymaps","plugin.program.community.builds","packages",".DS_Store",".setup_complete","XBMCHelper.conf")) #Create temp folder ready for zipping
    dp.close()
    FIX_SPECIAL(path)
    dialog.ok("Part 1 Complete", 'Successfully renamed your special paths and copied the', 'relevant files. If the following archiving process fails to', 'complete you can manually zip them up yourself on your PC, the files are located at: [COLOR=yellow]'+path+'[/COLOR]')
    backup_zip = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    ARCHIVE_FILE(path,backup_zip)
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Deleting temporary files",'', 'Please Wait')
    GUIname = xbmc.translatePath(os.path.join(fullbackuppath, title+'_guisettings.zip'))
    zf = zipfile.ZipFile(GUIname, mode='w')
    zf.write(xbmc.translatePath(os.path.join(path,'userdata','guisettings.xml')), 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
    try:
        zf.write(xbmc.translatePath(os.path.join(path,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
    except: pass
    zf.close()
    shutil.rmtree(path)
    dp.close()
    dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] Community Builds[/B]", 'You Are Now Backed Up. If you\'d like to share this build with', 'the community please post details on the forum at', '[COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')
#---------------------------------------------------------------------------------------------------
#Convert physical paths to special paths
def FIX_SPECIAL(url):
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(USERDATA, 'special://profile/').replace(ADDONS,'special://home/addons/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()
#---------------------------------------------------------------------------------------------------
#Backup the full XBMC system
def BACKUP():  
    choice = xbmcgui.Dialog().yesno("Are you sure you want this option?", 'This is a FULL Backup for personal use only. If you', 'want to create a build that works universally and can', 'be restored via the addon use the Community Build option.', yeslabel='Continue',nolabel='Cancel')
    if choice == 1:
        pass
    elif choice == 0:
        return        
    CHECK_DOWNLOAD_PATH()
    path = xbmc.translatePath(os.path.join(USB,'tempbackup'))
    fullbackuppath = xbmc.translatePath(os.path.join(USB,'Full Backup',''))
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    if os.path.exists(path):
        shutil.rmtree(path)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    # if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0
    # we need to set the title to our query
    title = urllib.quote_plus(vq)
    to_backup = xbmc.translatePath(HOME)
    backup_zip = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    DeletePackages()
    localfile = open(idfiletemp, mode='w+')
    localfile.write('id="Local"\nname="'+title+'"')
    localfile.close()
    ARCHIVE_FILE(to_backup,backup_zip)
    dialog.ok("Backup Complete", 'This is a FULL Backup for personal use only. It may', 'fail to restore via the addon, if you want a build that can', 'be restored via the addon use the Community Build option.')
#---------------------------------------------------------------------------------------------------
#Zip up tree
def ARCHIVE_FILE(sourcefile, destfile):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Archiving...",'', 'Please Wait')
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.community.builds' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
#Read a zip file and extract the relevant data
def READ_ZIP(url):

    import zipfile
    
    z = zipfile.ZipFile(url, "r")
    for filename in z.namelist():
        if 'guisettings.xml' in filename:
            a = z.read(filename)
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            
            match=re.compile(r).findall(a)
            print match
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
                
        if 'favourites.xml' in filename:
            a = z.read(filename)
            f = open(FAVS, mode='w')
            f.write(a)
            f.close()  
                           
        if 'sources.xml' in filename:
            a = z.read(filename)
            f = open(SOURCE, mode='w')
            f.write(a)
            f.close()    
                         
        if 'advancedsettings.xml' in filename:
            a = z.read(filename)
            f = open(ADVANCED, mode='w')
            f.write(a)
            f.close()                 

        if 'RssFeeds.xml' in filename:
            a = z.read(filename)
            f = open(RSS, mode='w')
            f.write(a)
            f.close()                 
            
        if 'keyboard.xml' in filename:
            a = z.read(filename)
            f = open(KEYMAPS, mode='w')
            f.write(a)
            f.close()                              
#---------------------------------------------------------------------------------------------------
def FACTORY(localbuildcheck,localversioncheck,id,unlocked):
    pass
    # if localbuildcheck == factoryname:
        # updatecheck = Check_For_Factory_Update(localbuildcheck,localversioncheck,id)
            # if updatecheck == True:
                    # addDir('[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','','','','')
                # else:
                    # addDir('[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','','','','')

#---------------------------------------------------------------------------------------------------
#Function to populate the search based on a second filter
def COMMUNITY2(url):
    print "COM2 START URL::"+str(url)
    link = OPEN_URL(url).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)"  <br> id="(.+?)"  <br> Thumbnail="(.+?)"  <br> Fanart="(.+?)"', re.DOTALL).findall(link)
    addBuildDir('[COLOR=lime]Add another filter to the search[/COLOR]',url,'genres2','genres.png','','','','','')
    for name,url,iconimage,fanart in match:
        addBuildDir(name,url,'community_menu',iconimage,fanart,'','','','')
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def grab_builds(url):
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your backup storage folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    username = ADDON.getSetting('username')
    password = ADDON.getSetting('password')
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        xbmcversion = 'gotham'
    else:
        xbmcversion = 'helix'

    if ADDON.getSetting('adult') == 'true':
        adult = ''
    else:
        adult = 'no'
    buildsURL = 'http://totalxbmc.tv/totalrevolution/Community_Builds/sortby.php?visibility=public&xbmc=%s&adult=%s&%s' % (xbmcversion, adult, url)
    print"URL: "+buildsURL
    link = OPEN_URL(buildsURL).replace('\n','').replace('\r','')
    if urlbase != 'None':
        addBuildDir('[COLOR=lime]Add another filter to the search[/COLOR]',urlbase,'genres2','genres.png','','','','','')
    match=re.compile('name="(.+?)"  <br> id="(.+?)"  <br> Thumbnail="(.+?)"  <br> Fanart="(.+?)"', re.DOTALL).findall(link)
    SortBy(buildsURL)
    for name,url,iconimage,fanart in match:
        addBuildDir(name,url,'community_menu',iconimage,fanart,'','','','')
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def PRIVATE_SEARCH(url):
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your backup storage folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        xbmcversion = 'gotham'
    else:
        xbmcversion = 'helix'

    if ADDON.getSetting('adult') == 'true':
        adult = ''
    else:
        adult = 'no'
    if url=='reseller':
        buildsURL = 'http://totalxbmc.tv/totalrevolution/Community_Builds/sortby.php?visibility=private&xbmc=%s&adult=%s&keyid=%s&username=%s' % (xbmcversion, adult, resellerid, resellername)	
    if url=='private':
        buildsURL = 'http://totalxbmc.tv/totalrevolution/Community_Builds/sortby.php?visibility=private&xbmc=%s&adult=%s&keyid=%s&username=%s' % (xbmcversion, adult, keyid, privateuser)
    print"URL: "+buildsURL
    link = OPEN_URL(buildsURL).replace('\n','').replace('\r','')
    if urlbase != 'None':
        addBuildDir('[COLOR=lime]Add another filter to the search[/COLOR]',urlbase,'genres2','genres.png','','','','','')
    match=re.compile('name="(.+?)"  <br> id="(.+?)"  <br> Thumbnail="(.+?)"  <br> Fanart="(.+?)"', re.DOTALL).findall(link)
    for name,url,iconimage,fanart in match:
        addBuildDir(name,url,'community_menu',iconimage,fanart,'','','','')
#---------------------------------------------------------------------------------------------------
#Function to read the contents of a URL
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
#---------------------------------------------------------------------------------------------------
#Function to restore a community build
def RESTORE_COMMUNITY(name,url,description,skins,guisettingslink):
    import time
    choice4=1
    CHECK_DOWNLOAD_PATH()
  #  lib=os.path.join(USB, 'guifix.zip')
    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    if not os.path.exists(tempfile): #Function for debugging, creates a file that was created in previous call and subsequently deleted when run
        localfile = open(tempfile, mode='w+')
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    try: os.rename(GUI,GUINEW) #Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    except:
        dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit XBMC and try again','')
        return
    choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before', 'installing any community builds.', 'Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
    if choice == 0:
        BACKUP()
    elif choice == 1:
        dialog.ok('Would you like to MERGE or WIPE?','You will now have the option to merge or wipe...','[COLOR=lime]1) MERGE[/COLOR] the new build with your existing setup (keeps your addons and settings).','[COLOR=red]2) WIPE[/COLOR] your existing install and install a fresh build.')
        choice2 = xbmcgui.Dialog().yesno(name, 'Would you like to merge with your existing build', 'or wipe your existing data and have a fresh', 'install with this new build?', nolabel='Merge',yeslabel='Wipe')
        if choice2 == 0: pass
        elif choice2 == 1:
            WipeInstall()
        if choice2 != 1 or (choice2 == 1 and skin == 'skin.confluence'):
            choice3 = xbmcgui.Dialog().yesno(name, 'Would you like to keep your existing database', 'files or overwrite? Overwriting will wipe any', 'existing library you may have scanned in.', nolabel='Overwrite',yeslabel='Keep Existing')
            if choice3 == 0: pass
            elif choice3 == 1:
                if os.path.exists(tempdbpath):
                    shutil.rmtree(tempdbpath)
                try:
                    shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library
                except:
                    choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases.', 'Continuing may wipe your existing library. Do you', 'wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
                    if choice4 == 1: pass
                    if choice4 == 0: return
                backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
                ARCHIVE_FILE(tempdbpath,backup_zip)
            if choice4 == 0: return
            time.sleep(1)
            dp.create("Community Builds","Downloading "+description +" build.",'', 'Please Wait')
            lib=os.path.join(CBPATH, description+'.zip')
            if not os.path.exists(CBPATH):
                os.makedirs(CBPATH)
            downloader.download(url, lib, dp)
            readfile = open(CBADDONPATH, mode='r')
            default_contents = readfile.read()
            readfile.close()
            READ_ZIP(lib)
            dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
            HOME = xbmc.translatePath(os.path.join('special://','home')) 
            dp.update(0,"", "Extracting Zip Please Wait")
            extract.all(lib,HOME,dp)
            time.sleep(1)
            localfile = open(tempfile, mode='r')
            content = file.read(localfile)
            file.close(localfile)
            temp = re.compile('id="(.+?)"').findall(content)
            tempcheck  = temp[0] if (len(temp) > 0) else ''
            tempname = re.compile('name="(.+?)"').findall(content)
            namecheck  = tempname[0] if (len(tempname) > 0) else ''
            tempversion = re.compile('version="(.+?)"').findall(content)
            versioncheck  = tempversion[0] if (len(tempversion) > 0) else ''
            writefile = open(idfile, mode='w+')
            writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+' [COLOR=yellow](Partially installed)[/COLOR]"\nversion="'+versioncheck+'"')
            writefile.close()
            incremental = 'http://totalxbmc.tv/totalrevolution/Community_Builds/downloadcount.php?id=%s' % (tempcheck)
            OPEN_URL(incremental)
            localfile = open(startuppath, mode='r')
            content = file.read(localfile)
            file.close(localfile)
            localversionmatch = re.compile('version="(.+?)"').findall(content)
            localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
            replacefile = content.replace(localversioncheck,versioncheck)
            writefile = open(startuppath, mode='w')
            writefile.write(str(replacefile))
            writefile.close()
            os.remove(tempfile)
            if localcopy == 'false':
                os.remove(lib)
            cbdefaultpy = open(CBADDONPATH, mode='w+')
            cbdefaultpy.write(default_contents)
            cbdefaultpy.close()
            try:
                os.rename(GUI,GUIFIX)
            except:
                print"NO GUISETTINGS DOWNLOADED"
            time.sleep(1)
            localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
            content = file.read(localfile)
            file.close(localfile)
            skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
            skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
            skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
            skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
            lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
            lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''
            try:
                localfile2 = open(GUIFIX, mode='r')
                content2 = file.read(localfile2)
                file.close(localfile2)
                skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
                skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
                skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
                skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
                lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
                lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
                replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
                writefile = open(GUINEW, mode='w+')
                writefile.write(str(replacefile))
                writefile.close()
            except:
                print"NO GUISETTINGS DOWNLOADED"
            if os.path.exists(GUI):
                os.remove(GUI)
            os.rename(GUINEW,GUI)
            try:
                os.remove(GUIFIX)
            except:
                pass
            if choice3 == 1:
                extract.all(backup_zip,DATABASE,dp) #This folder first needs zipping up
                if choice4 !=1:
                    shutil.rmtree(tempdbpath)
            #    os.remove(backup_zip)
            os.makedirs(guitemp)
            time.sleep(1)
            xbmc.executebuiltin('UnloadSkin()') 
            time.sleep(1)
            xbmc.executebuiltin('ReloadSkin()')
            time.sleep(1)
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            while xbmc.executebuiltin("Window.IsActive(appearancesettings)"):
                xbmc.sleep(500)
            try: xbmc.executebuiltin("LoadProfile(Master user)")
            except: pass
            dialog.ok('Step 1 complete','Change the skin to: [COLOR=lime]'+skins,'[/COLOR]Once done come back and choose install step 2 which will','re-install the guisettings.xml - this file contains all custom skin settings.')
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            CHECK_GUITEMP(guisettingslink)
#---------------------------------------------------------------------------------------------------
#Check whether or not the guisettings fix has been done, loops on a timer.
def CHECK_GUITEMP(url):
    time.sleep(120)
    if os.path.exists(guitemp):
        choice = xbmcgui.Dialog().yesno('Run step 2 of install', 'You still haven\'t completed step 2 of the', 'install. Would you like to complete it now?', '', nolabel='No, not yet',yeslabel='Yes, complete setup')
        if choice == 0:
            CHECK_GUITEMP(url)
        elif choice == 1:
            try: xbmc.executebuiltin("PlayerControl(Stop)")       
            except: pass
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            GUI_MERGE(url)
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def CHECK_DOWNLOAD_PATH():
#    if zip == '':
#        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
#        ADDON.openSettings(sys.argv[0])
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    if not os.path.exists(zip):
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','The download location you have stored does not exist .\nPlease update the addon settings and try again.','','')        
        ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def RESTORE():
    import time
    CHECK_DOWNLOAD_PATH()
    filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
    if filename == '':
        return
    localfile = open(idfiletemp, mode='w+')
    clean_title = ntpath.basename(filename)
    localfile.write('id="Local"\nname="'+clean_title+'"')
    localfile.close()
    READ_ZIP(filename)
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
    HOME = xbmc.translatePath(os.path.join('special://','home'))   
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(filename,HOME,dp)
    localfile = open(idfile, mode='w+')
    localfile.write('id="Local"\nname="Incomplete"')
    localfile.close()
    dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Step 1 complete. Now please change the skin to','the one this build was designed for. Once done come back','to this addon and click the link to complete the setup.')        
    xbmc.executebuiltin("ActivateWindow(appearancesettings)")
    # dialog.ok("Community Builds - Install Complete", 'To ensure the skin settings are set correctly XBMC will now', 'close. If XBMC doesn\'t close please force close (pull power', 'or force close in your OS - [COLOR=lime]DO NOT exit via XBMC menu[/COLOR])')
    # killxbmc()
#---------------------------------------------------------------------------------------------------
#Function to restore a local copy of a CB file
#### THIS CODE BLOCK SHOULD BE MERGED INTO THE RESTORE_COMMUNITY FUNCTION BUT I RAN OUT OF TIME TO DO IT CLEANLY ###
def RESTORE_LOCAL_COMMUNITY():
    import time
    exitfunction=0
    CHECK_DOWNLOAD_PATH()
    filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
    if filename == '':
        return
    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    if not os.path.exists(tempfile): #Function for debugging, creates a file that was created in previous call and subsequently deleted when run
        localfile = open(tempfile, mode='w+')
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    try: os.rename(GUI,GUINEW) #Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    except:
        dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit XBMC and try again','')
        return
    choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before', 'installing any community builds.', 'Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
    if choice == 0:
        BACKUP()
    elif choice == 1:
        dialog.ok('Would you like to MERGE or WIPE?','You will now have the option to merge or wipe...','[COLOR=lime]1) MERGE[/COLOR] the new build with your existing setup (keeps your addons and settings).','[COLOR=red]2) WIPE[/COLOR] your existing install and install a fresh build.')
        choice2 = xbmcgui.Dialog().yesno(name, 'Would you like to merge with your existing build', 'or wipe your existing data and have a fresh', 'install with this new build?', nolabel='Merge',yeslabel='Wipe')
        if choice2 == 0: pass
        elif choice2 == 1:
            WipeInstall()
        if choice2 != 1 or (choice2 == 1 and skin == 'skin.confluence'):
            choice3 = xbmcgui.Dialog().yesno(name, 'Would you like to keep your existing database', 'files or overwrite? Overwriting will wipe any', 'existing library you may have scanned in.', nolabel='Overwrite',yeslabel='Keep Existing')
            if choice3 == 0: pass
            elif choice3 == 1:
                if os.path.exists(tempdbpath):
                    shutil.rmtree(tempdbpath)
                try:
                    shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library
                except:
                    choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases.', 'Continuing may wipe your existing library. Do you', 'wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
                    if choice4 == 1: pass
                    if choice4 == 0: exitfunction=1;return
                backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
                ARCHIVE_FILE(tempdbpath,backup_zip)
            if exitfunction == 1: return
            time.sleep(1)
            readfile = open(CBADDONPATH, mode='r')
            default_contents = readfile.read()
            readfile.close()
            READ_ZIP(filename)
            dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
            HOME = xbmc.translatePath(os.path.join('special://','home')) 
            dp.update(0,"", "Extracting Zip Please Wait")
            extract.all(filename,HOME,dp)
            time.sleep(1)
            clean_title = ntpath.basename(filename)
            writefile = open(idfile, mode='w+')
            writefile.write('id="none"\nname="'+clean_title+' [COLOR=yellow](Partially installed)[/COLOR]"\nversion="none"')
            writefile.close()
            cbdefaultpy = open(CBADDONPATH, mode='w+')
            cbdefaultpy.write(default_contents)
            cbdefaultpy.close()
            try:
                os.rename(GUI,GUIFIX)
            except:
                print"NO GUISETTINGS DOWNLOADED"
            time.sleep(1)
            localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
            content = file.read(localfile)
            file.close(localfile)
            skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
            skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
            skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
            skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
            lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
            lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''
            try:
                localfile2 = open(GUIFIX, mode='r')
                content2 = file.read(localfile2)
                file.close(localfile2)
                skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
                skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
                skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
                skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
                lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
                lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
                replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
                writefile = open(GUINEW, mode='w+')
                writefile.write(str(replacefile))
                writefile.close()
            except:
                print"NO GUISETTINGS DOWNLOADED"
            if os.path.exists(GUI):
                os.remove(GUI)
            os.rename(GUINEW,GUI)
            try:
                os.remove(GUIFIX)
            except:
                pass
            if choice3 == 1:
                extract.all(backup_zip,DATABASE,dp) #This folder first needs zipping up
                if choice4 !=1:
                    shutil.rmtree(tempdbpath)
            #    os.remove(backup_zip)
            os.makedirs(guitemp)
            time.sleep(1)
            xbmc.executebuiltin('UnloadSkin()') 
            time.sleep(1)
            xbmc.executebuiltin('ReloadSkin()')
            time.sleep(1)
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            while xbmc.executebuiltin("Window.IsActive(appearancesettings)"):
                xbmc.sleep(500)
            try: xbmc.executebuiltin("LoadProfile(Master user)")
            except: pass
            dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Step 1 complete. Now please change the skin to','the one this build was designed for. Once done come back','to this addon and restore the guisettings_fix.zip')        
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
#---------------------------------------------------------------------------------------------------
#Function to restore a local copy of guisettings_fix
def RESTORE_LOCAL_GUI():
    import time
    CHECK_DOWNLOAD_PATH()
    guifilename = xbmcgui.Dialog().browse(1, 'Select the guisettings zip file you want to restore', 'files', '.zip', False, False, USB)
    if guifilename == '':
        return
    else:
        local=1
        GUISETTINGS_FIX(guifilename,local)  
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def REMOVE_BUILD():
    CHECK_DOWNLOAD_PATH()
    filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to DELETE', 'files', '.zip', False, False, USB)
    if filename == '':
        return
    clean_title = ntpath.basename(filename)
    choice = xbmcgui.Dialog().yesno('Delete Backup File', 'This will completely remove '+clean_title, 'Are you sure you want to delete?', '', nolabel='No, Cancel',yeslabel='Yes, Delete')
    if choice == 0:
        return
    elif choice == 1:
        os.remove(filename)
#---------------------------------------------------------------------------------------------------
#Kill Commands - these will make sure guisettings.xml sticks.
#ANDROID STILL NOT WORKING
def killxbmc():
    choice = xbmcgui.Dialog().yesno('Force Close XBMC/Kodi', 'We will now attempt to force close Kodi, this is', 'to be used if having problems with guisettings.xml', 'sticking. Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")
#---------------------------------------------------------------------------------------------------
#Root menu of addon
def CATEGORIES(localbuildcheck,localversioncheck,id,unlocked):
#    if os.path.exists(factory):
#        FACTORY()
    if reseller=='true':
        addDir('[COLOR=yellow]Check for new '+resellername+' Builds[/COLOR]','reseller','Search_Private','TRCOMMUNITYHELIXBUILDS.png','','','')        
    if unlocked == 'yes':
        if id != 'None':
            if id != 'Local':
                updatecheck = Check_For_Update(localbuildcheck,localversioncheck,id)
                if updatecheck == True:
                    addDir('[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','TOTALXBMC.png','','','')
                else:
                    addDir('[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','TOTALXBMC.png','','','')
            else:
                if localbuildcheck == 'Incomplete':
                    addDir('[COLOR=lime]Your last restore is not yet completed[/COLOR]','url',CHECK_LOCAL_INSTALL(),'TOTALXBMC.png','','','')
                else:
                    addDir('[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]Local Build ('+localbuildcheck+')[/COLOR]','TOTALXBMC.png','','','','','')
    else:
        addDir('[COLOR=lime]REGISTER FOR FREE TO UNLOCK FEATURES[/COLOR]','None','Register','TOTALXBMC.png','','','')
    addDir('[COLOR=orange]How To Use This Addon[/COLOR]','url','instructions','How_To.png','','','Instructions')
    addDir('Addon Settings','settings','Addon_Settings','SETTINGS.png','','','Addon Settings')
    addDir('Install Community Build','none','cb_root_menu','Community_Builds.png','','','Install Community Build')
    addDir('Backup My Content','url','backup_option','Backup.png','','','Back Up Your Data')
    addDir('Restore My Content','url','restore_option','Restore.png','','','Restore Your Data')
    addDir('Additional Tools','url','additional_tools','Additional_Tools.png','','','Restore Your Data')
#---------------------------------------------------------------------------------------------------
# Dialog to tell users how to register
def Register():
    dialog.ok("Register to unlock features", "To get the most out of this addon please register at", "the TotalXBMC forum where the addon is developed.","Visit [COLOR=lime]www.totalxbmc.tv/new-forum[/COLOR] for more details.")
#---------------------------------------------------------------------------------------------------
# Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
# Extra tools menu
def ADDITIONAL_TOOLS():
    addDir('Delete Builds From Device','url','remove_build','Delete_Builds.png','','','Delete Build')
    addDir('Wipe My Setup (Fresh Start)','url','wipe_xbmc','Fresh_Start.png','','','Wipe your special XBMC/Kodi directory which will revert back to a vanillla build.')
    addDir('Convert Physical Paths To Special',HOME,'fix_special','Special_Paths.png','','','Convert Physical Paths To Special')
    addDir('Force Close Kodi','url','kill_xbmc','Kill_XBMC.png','','','Force close kodi, to be used as last resort')
#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def SHOWINFO(url):
    BaseURL='http://totalxbmc.tv/totalrevolution/Community_Builds/community_builds.php?id=%s' % (url)
    link = OPEN_URL(BaseURL).replace('\n','').replace('\r','')
    namematch = re.compile('name="(.+?)"').findall(link)
    authormatch = re.compile('author="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    updatedmatch = re.compile('updated="(.+?)"').findall(link)
    name  = namematch[0] if (len(namematch) > 0) else ''
    author  = authormatch[0] if (len(authormatch) > 0) else ''
    version  = versionmatch[0] if (len(versionmatch) > 0) else ''
    updated  = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    dialog.ok(name,'Author: '+author,'Latest Version: '+version,'Latest Update: '+updated)
    return
#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def Check_For_Update(localbuildcheck,localversioncheck,id):
    print "Local Version Check: "+localversioncheck
 #   if localbuildcheck == factoryname: pass

    BaseURL = 'http://totalxbmc.tv/totalrevolution/Community_Builds/buildupdate.php?id=%s' % (id)
    link = OPEN_URL(BaseURL).replace('\n','').replace('\r','')
    if id != 'None':
        versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    if  localversioncheck < versioncheck:
        print "local build: "+str(localbuildcheck)
        print "new version available"
        return True
    else:
        return False
        print "local build: "+str(localbuildcheck)
        print "all good in the hood"
#---------------------------------------------------------------------------------------------------
#Build the root search menu for installing community builds
def CB_Root_Menu():
    logged_in = weblogin.doLogin(cookiepath,username,password)
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if login == 'true':
        if logged_in == True:
            if privatebuilds=='true':
                addDir('[COLOR=lime]Show My Private List[/COLOR]','private','Search_Private','TRCOMMUNITYHELIXBUILDS.png','','','')        
            addDir('Manual Search','url','manual_search','Manual_Search.png','','','')
            addDir('Search By Genre','url','genres','Search_Genre.png','','','')
            addDir('Search By Country/Language','url','countries','Search_Country.png','','','')
            if version < 14:
                addDir('Show All Gotham Compatible Builds','genre=','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
            else:
                addDir('Show All Helix Compatible Builds','genre=','grab_builds','TRCOMMUNITYHELIXBUILDS.png','','','')
            addDir('Restore a locally stored Community Build','url','restore_local_CB','Restore.png','','','Back Up Your Full System')
        elif logged_in == False:
            dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','There is an error with your login information, please check','your username and password, remember this is case','sensitive so use capital letters where needed.')
            ADDON.openSettings(sys.argv[0])
    else:
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','[COLOR=blue][B]Did you know you\'re missing out of some great features?[/B][/COLOR]','To unlock this content simply register on the forum for [COLOR=yellow]FREE[/COLOR]','at [COLOR=lime]www.totalxbmc.tv[/COLOR] and enter details in the addon settings.')
        if version < 14:
            addDir('Show All Gotham Compatible Builds','genre=','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
        else:
            addDir('Show All Helix Compatible Builds','genre=','grab_builds','TRCOMMUNITYHELIXBUILDS.png','','','')       
        addDir('Restore a locally stored Community Build','url','restore_local_CB','Restore.png','','','Back Up Your Full System')
#---------------------------------------------------------------------------------------------------
#Search in description
def MANUAL_SEARCH():
    addDir('Search By Name','name','search_builds','Manual_Search.png','','','')
    addDir('Search By Uploader','author','search_builds','Search_Genre.png','','','')
    addDir('Search By Audio Addons Installed','audio','search_builds','Search_Addons.png','','','')
    addDir('Search By Picture Addons Installed','pics','search_builds','Search_Addons.png','','','')
    addDir('Search By Program Addons Installed','progs','search_builds','Search_Addons.png','','','')
    addDir('Search By Video Addons Installed','vids','search_builds','Search_Addons.png','','','')
    addDir('Search By Skins Installed','skins','search_builds','Search_Addons.png','','','')
#---------------------------------------------------------------------------------------------------
#Search in description
def SEARCH_BUILDS():
    if url == 'name':
        searchUrl = 'name='
    elif url == 'author':
        searchUrl = 'author='
    elif url == 'audio':
        searchUrl = 'audio='
    elif url == 'pics':
        searchUrl = 'pics='
    elif url == 'progs':
        searchUrl = 'progs='
    elif url == 'vids':
        searchUrl = 'vids='
    elif url == 'skins':
        searchUrl = 'skins='
    vq = _get_keyboard( heading="Search for content" )
    # if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0
    # we need to set the title to our query
    title = urllib.quote_plus(vq)
    searchUrl += title
    print "Searching URL: " + searchUrl 
    grab_builds(searchUrl)
#---------------------------------------------------------------------------------------------------
# menu to set the sort type when searching
def SortBy(url):       
    urlbase = url
    addDir2('[COLOR=dodgerblue]Sort by Most Popular[/COLOR]',url+'&sortx=downloadcount&orderx=DESC','grab_builds','Popular.png','','','')
    addDir2('[COLOR=dodgerblue]Sort by Newest Builds[/COLOR]',url+'&sortx=created&orderx=DESC','grab_builds','Latest.png','','','')
    addDir2('[COLOR=dodgerblue]Sort by Recently Updated[/COLOR]',url+'&sortx=updated&orderx=DESC','grab_builds','Recently_Updated.png','','','')
    addDir2('[COLOR=dodgerblue]Sort by A-Z[/COLOR]',url+'&sortx=name&orderx=ASC','grab_builds','AtoZ.png','','','')
    addDir2('[COLOR=dodgerblue]Sort by Z-A[/COLOR]',url+'&sortx=name&orderx=DESC','grab_builds','ZtoA.png','','','')
#---------------------------------------------------------------------------------------------------
#Get keyboard
def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default
#-----------------------------------------------------------------------------------------------------------------    
#Build Genres Menu (First Filter)
def GENRES():       
    addDir('Anime','genre=anime','grab_builds','anime.png','','','')
    addDir('Audiobooks','genre=audiobooks','grab_builds','audiobooks.png','','','')
    addDir('Comedy','genre=comedy','grab_builds','comedy.png','','','')
    addDir('Comics','genre=comics','grab_builds','comics.png','','','')
    addDir('Documentary','genre=documentary','grab_builds','documentary.png','','','')
    addDir('Downloads','genre=downloads','grab_builds','downloads.png','','','')
    addDir('Food','genre=food','grab_builds','food.png','','','')
    addDir('Gaming','genre=gaming','grab_builds','gaming.png','','','')
    addDir('Health','genre=health','grab_builds','health.png','','','')
    addDir('How To...','genre=howto','grab_builds','howto.png','','','')
    addDir('Kids','genre=kids','grab_builds','kids.png','','','')
    addDir('Live TV','genre=livetv','grab_builds','livetv.png','','','')
    addDir('Movies','genre=movies','grab_builds','movies.png','','','')
    addDir('Music','genre=music','grab_builds','music.png','','','')
    addDir('News','genre=news','grab_builds','news.png','','','')
    addDir('Photos','genre=photos','grab_builds','photos.png','','','')
    addDir('Podcasts','genre=podcasts','grab_builds','podcasts.png','','','')
    addDir('Radio','genre=radio','grab_builds','radio.png','','','')
    addDir('Religion','genre=religion','grab_builds','religion.png','','','')
    addDir('Space','genre=space','grab_builds','space.png','','','')
    addDir('Sports','genre=sports','grab_builds','sports.png','','','')
    addDir('Technology','genre=tech','grab_builds','tech.png','','','')
    addDir('Trailers','genre=trailers','grab_builds','trailers.png','','','')
    addDir('TV Shows','genre=tv','grab_builds','tv.png','','','')
    addDir('Misc.','genre=other','grab_builds','other.png','','','')
    if ADDON.getSetting('adult') == 'true':
        addDir('XXX','genre=adult','grab_builds','adult.png','','','')
#---------------------------------------------------------------------------------------------------
#Build Countries Menu (First Filter)    
def COUNTRIES():
    addDir('African','genre=african','grab_builds','african.png','','','')
    addDir('Arabic','genre=arabic','grab_builds','arabic.png','','','')
    addDir('Asian','genre=asian','grab_builds','asian.png','','','')
    addDir('Australian','genre=australian','grab_builds','australian.png','','','')
    addDir('Austrian','genre=austrian','grab_builds','austrian.png','','','')
    addDir('Belgian','genre=belgian','grab_builds','belgian.png','','','')
    addDir('Brazilian','genre=brazilian','grab_builds','brazilian.png','','','')
    addDir('Canadian','genre=canadian','grab_builds','canadian.png','','','')
    addDir('Columbian','genre=columbian','grab_builds','columbian.png','','','')
    addDir('Czech','genre=czech','grab_builds','czech.png','','','')
    addDir('Danish','genre=danish','grab_builds','danish.png','','','')
    addDir('Dominican','genre=dominican','grab_builds','dominican.png','','','')
    addDir('Dutch','genre=dutch','grab_builds','dutch.png','','','')
    addDir('Egyptian','genre=egyptian','grab_builds','egyptian.png','','','')
    addDir('Filipino','genre=filipino','grab_builds','filipino.png','','','')
    addDir('Finnish','genre=finnish','grab_builds','finnish.png','','','')
    addDir('French','genre=french','grab_builds','french.png','','','')
    addDir('German','genre=german','grab_builds','german.png','','','')
    addDir('Greek','genre=greek','grab_builds','greek.png','','','')
    addDir('Hebrew','genre=hebrew','grab_builds','hebrew.png','','','')
    addDir('Hungarian','genre=hungarian','grab_builds','hungarian.png','','','')
    addDir('Icelandic','genre=icelandic','grab_builds','icelandic.png','','','')
    addDir('Indian','genre=indian','grab_builds','indian.png','','','')
    addDir('Irish','genre=irish','grab_builds','irish.png','','','')
    addDir('Italian','genre=italian','grab_builds','italian.png','','','')
    addDir('Japanese','genre=japanese','grab_builds','japanese.png','','','')
    addDir('Korean','genre=korean','grab_builds','korean.png','','','')
    addDir('Lebanese','genre=lebanese','grab_builds','lebanese.png','','','')
    addDir('Mongolian','genre=mongolian','grab_builds','mongolian.png','','','')
    addDir('Nepali','genre=nepali','grab_builds','nepali.png','','','')
    addDir('New Zealand','genre=newzealand','grab_builds','newzealand.png','','','')
    addDir('Norwegian','genre=norwegian','grab_builds','norwegian.png','','','')
    addDir('Pakistani','genre=pakistani','grab_builds','pakistani.png','','','')
    addDir('Polish','genre=polish','grab_builds','polish.png','','','')
    addDir('Portuguese','genre=portuguese','grab_builds','portuguese.png','','','')
    addDir('Romanian','genre=romanian','grab_builds','romanian.png','','','')
    addDir('Russian','genre=russian','grab_builds','russian.png','','','')
    addDir('Singapore','genre=singapore','grab_builds','singapore.png','','','')
    addDir('Spanish','genre=spanish','grab_builds','spanish.png','','','')
    addDir('Swedish','genre=swedish','grab_builds','swedish.png','','','')
    addDir('Swiss','genre=swiss','grab_builds','swiss.png','','','')
    addDir('Syrian','genre=syrian','grab_builds','syrian.png','','','')
    addDir('Tamil','genre=tamil','grab_builds','tamil.png','','','')
    addDir('Thai','genre=thai','grab_builds','thai.png','','','')
    addDir('Turkish','genre=turkish','grab_builds','turkish.png','','','')
    addDir('UK','genre=uk','grab_builds','uk.png','','','')
    addDir('USA','&genre=usa','grab_builds','usa.png','','','')
    addDir('Vietnamese','genre=vietnamese','grab_builds','vietnamese.png','','','')
#---------------------------------------------------------------------------------------------------
#Build Countries and Genre Menu (Second Filter)    
def GENRES2(url):       
    addDir('[COLOR=lime]GENRES[/COLOR]','None','None','genres.png','','','')
    addDir('Anime',url+',anime','grab_builds2','anime.png','','','')
    addDir('Audiobooks',url+',audiobooks','grab_builds2','audiobooks.png','','','')
    addDir('Comedy',url+',comedy','grab_builds2','comedy.png','','','')
    addDir('Comics',url+',comics','grab_builds2','comics.png','','','')
    addDir('Documentary',url+',documentary','grab_builds2','documentary.png','','','')
    addDir('Downloads',url+',downloads','grab_builds2','downloads.png','','','')
    addDir('Food',url+',food','grab_builds2','food.png','','','')
    addDir('Gaming',url+',gaming','grab_builds2','gaming.png','','','')
    addDir('Health',url+',health','grab_builds2','health.png','','','')
    addDir('How To...',url+',howto','grab_builds2','howto.png','','','')
    addDir('Kids',url+',kids','grab_builds2','kids.png','','','')
    addDir('Live TV',url+',livetv','grab_builds2','livetv.png','','','')
    addDir('Movies',url+',movies','grab_builds2','movies.png','','','')
    addDir('Music',url+',music','grab_builds2','music.png','','','')
    addDir('News',url+',news','grab_builds2','news.png','','','')
    addDir('Photos',url+',photos','grab_builds2','photos.png','','','')
    addDir('Podcasts',url+',podcasts','grab_builds2','podcasts.png','','','')
    addDir('Radio',url+',radio','grab_builds2','radio.png','','','')
    addDir('Religion',url+',religion','grab_builds2','religion.png','','','')
    addDir('Space',url+',space','grab_builds2','space.png','','','')
    addDir('Sports',url+',sports','grab_builds2','sports.png','','','')
    addDir('Technology',url+',tech','grab_builds2','tech.png','','','')
    addDir('Trailers',url+',trailers','grab_builds2','trailers.png','','','')
    addDir('TV Shows',url+',tv','grab_builds2','tv.png','','','')
    addDir('Misc.',url+',other','grab_builds2','other.png','','','')
    if ADDON.getSetting('adult') == 'true':
        addDir('XXX','genre2=adult','grab_builds2','adult.png','','','')
    addDir('[COLOR=lime]COUNTRIES[/COLOR]','None','None','countries.png','','','')
    addDir('African',url+',african','grab_builds2','african.png','','','')
    addDir('Arabic',url+',arabic','grab_builds2','arabic.png','','','')
    addDir('Asian',url+',asian','grab_builds2','asian.png','','','')
    addDir('Australian',url+',australian','grab_builds2','australian.png','','','')
    addDir('Austrian',url+',austrian','grab_builds2','austrian.png','','','')
    addDir('Belgian',url+',belgian','grab_builds2','belgian.png','','','')
    addDir('Brazilian',url+',brazilian','grab_builds2','brazilian.png','','','')
    addDir('Canadian',url+',canadian','grab_builds2','canadian.png','','','')
    addDir('Columbian',url+',columbian','grab_builds2','columbian.png','','','')
    addDir('Czech',url+',czech','grab_builds2','czech.png','','','')
    addDir('Danish',url+',danish','grab_builds2','danish.png','','','')
    addDir('Dominican',url+',dominican','grab_builds2','dominican.png','','','')
    addDir('Dutch',url+',dutch','grab_builds2','dutch.png','','','')
    addDir('Egyptian',url+',egyptian','grab_builds2','egyptian.png','','','')
    addDir('Filipino',url+',filipino','grab_builds2','filipino.png','','','')
    addDir('Finnish',url+',finnish','grab_builds2','finnish.png','','','')
    addDir('French',url+',french','grab_builds2','french.png','','','')
    addDir('German',url+',german','grab_builds2','german.png','','','')
    addDir('Greek',url+',greek','grab_builds2','greek.png','','','')
    addDir('Hebrew',url+',hebrew','grab_builds2','hebrew.png','','','')
    addDir('Hungarian',url+',hungarian','grab_builds2','hungarian.png','','','')
    addDir('Icelandic',url+',icelandic','grab_builds2','icelandic.png','','','')
    addDir('Indian',url+',indian','grab_builds2','indian.png','','','')
    addDir('Irish',url+',irish','grab_builds2','irish.png','','','')
    addDir('Italian',url+',italian','grab_builds2','italian.png','','','')
    addDir('Japanese',url+',japanese','grab_builds2','japanese.png','','','')
    addDir('Korean',url+',korean','grab_builds2','korean.png','','','')
    addDir('Lebanese',url+',lebanese','grab_builds2','lebanese.png','','','')
    addDir('Mongolian',url+',mongolian','grab_builds2','mongolian.png','','','')
    addDir('Nepali',url+',nepali','grab_builds2','nepali.png','','','')
    addDir('New Zealand',url+',newzealand','grab_builds2','newzealand.png','','','')
    addDir('Norwegian',url+',norwegian','grab_builds2','norwegian.png','','','')
    addDir('Pakistani',url+',pakistani','grab_builds2','pakistani.png','','','')
    addDir('Polish',url+',polish','grab_builds2','polish.png','','','')
    addDir('Portuguese',url+',portuguese','grab_builds2','portuguese.png','','','')
    addDir('Romanian',url+',romanian','grab_builds2','romanian.png','','','')
    addDir('Russian',url+',russian','grab_builds2','russian.png','','','')
    addDir('Singapore',url+',singapore','grab_builds2','singapore.png','','','')
    addDir('Spanish',url+',spanish','grab_builds2','spanish.png','','','')
    addDir('Swedish',url+',swedish','grab_builds2','swedish.png','','','')
    addDir('Swiss',url+',swiss','grab_builds2','swiss.png','','','')
    addDir('Syrian',url+',syrian','grab_builds2','syrian.png','','','')
    addDir('Tamil',url+',tamil','grab_builds2','tamil.png','','','')
    addDir('Thai',url+',thai','grab_builds2','thai.png','','','')
    addDir('Turkish',url+',turkish','grab_builds2','turkish.png','','','')
    addDir('UK',url+',uk','grab_builds2','uk.png','','','')
    addDir('USA',url+',usa','grab_builds2','usa.png','','','')
    addDir('Vietnamese',url+',vietnamese','grab_builds2','vietnamese.png','','','')
#---------------------------------------------------------------------------------------------------
#Call the yt module for playing videos. Thanks to spoyser for this module.
def PLAYVIDEO(url):
    import yt    
    yt.PlayVideo(url)
#---------------------------------------------------------------------------------------------------
#Create How To (instructions) menu
def INSTRUCTIONS(url):
    addDir('[COLOR=dodgerblue][TEXT GUIDE][/COLOR] What is Community Builds?','url','instructions_3','How_To.png','','','')
    addDir('[COLOR=dodgerblue][TEXT GUIDE][/COLOR] Creating a Community Build','url','instructions_1','How_To.png','','','')
    addDir('[COLOR=dodgerblue][TEXT GUIDE][/COLOR] Installing a Community Build','url','instructions_2','How_To.png','','','')
    addDir('[COLOR=lime][VIDEO GUIDE][/COLOR] IMPORTANT initial settings',"1vXniHsEMEg",'play_video','howto.png','','','')
    addDir('[COLOR=lime][VIDEO GUIDE][/COLOR] Install a Community Build',"kLsVOapuM1A",'play_video','howto.png','','','')
    addDir('[COLOR=lime][VIDEO GUIDE][/COLOR] Fixing a half installed build (guisettings.xml fix)',"X8QYLziFzQU",'play_video','howto.png','','','')
    addDir('[COLOR=lime][VIDEO GUIDE][/COLOR] [COLOR=yellow](OLD METHOD)[/COLOR]Create a Community Build (part 1)',"3rMScZF2h_U",'play_video','howto.png','','','')
    addDir('[COLOR=lime][VIDEO GUIDE][/COLOR] [COLOR=yellow](OLD METHOD)[/COLOR]Create a Community Build (part 2)',"C2IPhn0OSSw",'play_video','howto.png','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Submitting A Community Backup[/COLOR]','url',16,'','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Creating A Local Backup[/COLOR]','url',17,'','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Restoring A Local Backup[/COLOR]','url',18,'','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Fresh Start XBMC/Kodi[/COLOR]','url',19,'','','','')
#---------------------------------------------------------------------------------------------------
#(Instructions) Create a community backup
def Instructions_1():
    TextBoxes('Creating A Community Backup', 
    '[COLOR=yellow]NEW METHOD[/COLOR][CR][COLOR=blue][B]Step 1:[/COLOR] Remove any sensitive data[/B][CR]Make sure you\'ve removed any sensitive data such as passwords and usernames in your addon_data folder.'
    '[CR][CR][COLOR=blue][B]Step 2:[/COLOR] Backup your system[/B][CR]Choose the backup option from the main menu, in there you\'ll find the option to create a Community Build and this will create two zip files that you need to upload to a server.'
    '[CR][CR][COLOR=blue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip files to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - Dropbox and archive.org are two good examples.'
    '[CR][CR][COLOR=blue][B]Step 4:[/COLOR] Submit build at TotalXBMC[/B]'
    '[CR]Create a thread on the Community Builds section of the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B].[CR]Full details can be found on there of the template you should use when posting.'
    '[CR][CR][COLOR=yellow]OLD METHOD[/COLOR][CR][COLOR=blue][B]Step 1: Backup your system[/B][/COLOR][CR]Choose the backup option from the main menu, you will be asked whether you would like to delete your addon_data folder. If you decide to choose this option [COLOR=yellow][B]make sure[/COLOR][/B] you already have a full backup of your system as it will completely wipe your addon settings (any stored settings such as passwords or any other changes you\'ve made to addons since they were first installed). If sharing a build with the community it\'s highly advised that you wipe your addon_data but if you\'ve made changes or installed extra data packages (e.g. skin artwork packs) then backup the whole build and then manually delete these on your PC and zip back up again (more on this later).'
    '[CR][CR][COLOR=blue][B]Step 2: Edit zip file on your PC[/B][/COLOR][CR]Copy your backup.zip file to your PC, extract it and delete all the addons and addon_data that isn\'t required.'
    '[CR][COLOR=blue]What to delete:[/COLOR][CR][COLOR=lime]/addons/packages[/COLOR] This folder contains zip files of EVERY addon you\'ve ever installed - it\'s not needed.'
    '[CR][COLOR=lime]/addons/<skin.xxx>[/COLOR] Delete any skins that aren\'t used, these can be very big files.'
    '[CR][COLOR=lime]/addons/<addon_id>[/COLOR] Delete any other addons that aren\'t used, it\'s easy to forget you\'ve got things installed that are no longer needed.'
    '[CR][COLOR=lime]/userdata/addon_data/<addon_id>[/COLOR] Delete any folders that don\'t contain important changes to addons. If you delete these the associated addons will just reset to their default values.'
    '[CR][COLOR=lime]/userdata/<all other folders>[/COLOR] Delete all other folders in here such as keymaps. If you\'ve setup profiles make sure you [COLOR=yellow][B]keep the profiles directory[/COLOR][/B].'
    '[CR][COLOR=lime]/userdata/Thumbnails/[/COLOR] Delete this folder, it contains all cached artwork. You can safely delete this but must also delete the file listed below.'
    '[CR][COLOR=lime]/userdata/Database/Textures13.db[/COLOR] Delete this and it will tell XBMC to regenerate your thumbnails - must do this if delting thumbnails folder.'
    '[CR][COLOR=lime]/xbmc.log (or Kodi.log)[/COLOR] Delete your log files, this includes any crashlog files you may have.'
    '[CR][CR][COLOR=blue][B]Step 3: Compress and upload[/B][/COLOR][CR]Use a program like 7zip to create a zip file of your remaining folders and upload to a file sharing site like dropbox.'
    '[CR][CR][COLOR=blue][B]Step 4: Submit build at TotalXBMC[/B][/COLOR]'
    '[CR]Create a thread on the Community Builds section of the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B].[CR]Full details can be found on there of the template you should use when posting.')
 #---------------------------------------------------------------------------------------------------
#(Instructions) Install a community build   
def Instructions_2():
    TextBoxes('Installing a community build', '[COLOR=blue][B]Step 1 (Optional): Backup your system[/B][/COLOR][CR]We highly recommend creating a backup of your system in case you don\'t like the build and want to revert back. Choose the backup option from the main menu, you will be asked whether you would like to delete your addon_data folder, select no unless you want to lose all your settings. If you ever need your backup it\'s stored in the location you\'ve selected in the addon settings.'
    '[CR][CR][COLOR=blue][B]Step 2: Browse the Community Builds[/B][/COLOR][CR]Find a community build you like the look of and make sure you read the description as it could contain unsuitable content or have specific install instructions. Once you\'ve found the build you want to install click on the install option and you\'ll have the option of a fresh install or a merge . The merge option will leave all your existing addons and userdata in place and just add the contents of the new build whereas the fresh (wipe) option will completely wipe your existing data and replace with content on the new build. Once you make your choice the download and extraction process will begin.'
    '[CR][CR][COLOR=blue][B]Step 3: [/COLOR][COLOR=red]VERY IMPORTANT[/COLOR][/B][CR]For the install to complete properly you MUST change the skin to the relevant skin used for that build. You will see a dialog box telling you which skin to switch to and then you\'ll be taken to the appearance settings where you can switch skins.'
    '[CR][CR][COLOR=blue][B]Step 4:[/B][/COLOR] Now go back to the Community Builds addon and in the same section wehre you clicked on step 1 of the install process you now need to select step 2 so it can install the guisettings.xml. This is extremely important, if you don\'t do this step then you\'ll end up with a real mish-mash hybrid install!'
    '[CR][CR][COLOR=blue][B]Step 5:[/B][/COLOR] You will now need to restart Kodi so the settings stick, just quit and it should all be fine. If for any reason the settings did not stick and it still doesn\'t look quite right just do step 2 of the install process again (guisettings.xml fix)')
    #---------------------------------------------------------------------------------------------------
#(Instructions) What is a community build
def Instructions_3():
    TextBoxes('What is a community build', 'Community Builds are pre-configured builds of XBMC/Kodi based on different users setups. Have you ever watched youtube videos or seen screenshots of Kodi in action and thought "wow I wish I could do that"? Well now you can have a brilliant setup at the click of a button, completely pre-configured by users on the [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B] forum. If you\'d like to get involved yourself and share your build with the community it\'s very simple to do, just go to the forum where you\'ll find full details or you can follow the guide in this addon.')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def COMMUNITY_MENU(url):
    BaseURL='http://totalxbmc.tv/totalrevolution/Community_Builds/community_builds.php?id=%s' % (url)
    link = OPEN_URL(BaseURL).replace('\n','').replace('\r','')
    videopreviewmatch = re.compile('videopreview="(.+?)"').findall(link)
    videoguide1match = re.compile('videoguide1="(.+?)"').findall(link)
    videoguide2match = re.compile('videoguide2="(.+?)"').findall(link)
    videoguide3match = re.compile('videoguide3="(.+?)"').findall(link)
    videoguide4match = re.compile('videoguide4="(.+?)"').findall(link)
    videoguide5match = re.compile('videoguide5="(.+?)"').findall(link)
    videolabel1match = re.compile('videolabel1="(.+?)"').findall(link)
    videolabel2match = re.compile('videolabel2="(.+?)"').findall(link)
    videolabel3match = re.compile('videolabel3="(.+?)"').findall(link)
    videolabel4match = re.compile('videolabel4="(.+?)"').findall(link)
    videolabel5match = re.compile('videolabel5="(.+?)"').findall(link)
    namematch = re.compile('name="(.+?)"').findall(link)
    authormatch = re.compile('author="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    descmatch = re.compile('description="(.+?)"').findall(link)
    downloadmatch = re.compile('DownloadURL="(.+?)"').findall(link)
    updatedmatch = re.compile('updated="(.+?)"').findall(link)
    defaultskinmatch = re.compile('defaultskin="(.+?)"').findall(link)
    skinsmatch = re.compile('skins="(.+?)"').findall(link)
    videoaddonsmatch = re.compile('videoaddons="(.+?)"').findall(link)
    audioaddonsmatch = re.compile('audioaddons="(.+?)"').findall(link)
    programaddonsmatch = re.compile('programaddons="(.+?)"').findall(link)
    pictureaddonsmatch = re.compile('pictureaddons="(.+?)"').findall(link)
    sourcesmatch = re.compile('sources="(.+?)"').findall(link)
    adultmatch = re.compile('adult="(.+?)"').findall(link)
    guisettingsmatch = re.compile('guisettings="(.+?)"').findall(link)
   
    name  = namematch[0] if (len(namematch) > 0) else ''
    author  = authormatch[0] if (len(authormatch) > 0) else ''
    version  = versionmatch[0] if (len(versionmatch) > 0) else ''
    description  = descmatch[0] if (len(descmatch) > 0) else 'No information available'
    updated = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    defaultskin = defaultskinmatch[0] if (len(defaultskinmatch) > 0) else ''
    skins = skinsmatch[0] if (len(skinsmatch) > 0) else ''
    videoaddons = videoaddonsmatch[0] if (len(videoaddonsmatch) > 0) else ''
    audioaddons = audioaddonsmatch[0] if (len(audioaddonsmatch) > 0) else ''
    programaddons = programaddonsmatch[0] if (len(programaddonsmatch) > 0) else ''
    pictureaddons = pictureaddonsmatch[0] if (len(pictureaddonsmatch) > 0) else ''
    sources = sourcesmatch[0] if (len(sourcesmatch) > 0) else ''
    adult = adultmatch[0] if (len(adultmatch) > 0) else ''
    guisettingslink = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    downloadURL  = downloadmatch[0] if (len(downloadmatch) > 0) else 'None'
    videopreview  = videopreviewmatch[0] if (len(videopreviewmatch) > 0) else 'None'
    videoguide1  = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2  = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3  = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4  = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5  = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1  = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2  = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3  = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4  = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5  = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    localfile = open(tempfile, mode='w+')
    localfile.write('id="'+url+'"\nname="'+name+'"\nversion="'+version+'"')
    localfile.close()
    print"preview: "+videopreview
    print"guide1: "+videoguide1
    print"guide2: "+videoguide2
    print"guide3: "+videoguide3
    print"guide4: "+videoguide4
    print"guide5: "+videoguide5
    addDescDir('Full description','None','description','BUILDDETAILS.png',fanart,name,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    if videopreview != 'None':
        addDir('Watch Preview Video',videopreview,'play_video','Video_Preview.png',fanart,'','')
    if videoguide1 != 'None':
        addDir('(VIDEO) '+videolabel1,videoguide1,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide2 != 'None':
        addDir('(VIDEO) '+videolabel2,videoguide2,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide3 != 'None':
        addDir('(VIDEO) '+videolabel3,videoguide3,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide4 != 'None':
        addDir('(VIDEO) '+videolabel4,videoguide4,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide5 != 'None':
        addDir('(VIDEO) '+videolabel5,videoguide5,'play_video','Video_Guide.png',fanart,'','')    
    if downloadURL=='None':
        addBuildDir('[COLOR=gold]Sorry this build is currently unavailable[COLOR]','','','','','','','','')
    else:
        addBuildDir('[COLOR=lime]Install 1: Download '+name+'[/COLOR]',downloadURL,'restore_community',iconimage,fanart,'',name,defaultskin,guisettingslink)
    if guisettingslink=='None':
        pass
    else:
        addDir('[COLOR=dodgerblue]Install 2: Apply guisettings.xml fix[/COLOR]',guisettingslink,'guisettingsfix','FixMy_Build.png',fanart,'','')
#---------------------------------------------------------------------------------------------------
#Option to download guisettings fix that merges with existing settings.
def GUISETTINGS_FIX(url,local):
    CHECK_DOWNLOAD_PATH()
    choice = xbmcgui.Dialog().yesno(name, 'This will over-write your existing guisettings.xml.', 'Are you sure this is the build you have installed?', '', nolabel='No, Cancel',yeslabel='Yes, Fix')
    if choice == 0:
        return
    elif choice == 1:
        GUI_MERGE(url,local)
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
def INSTALL_PART2(url):
    BaseURL='http://totalxbmc.tv/totalrevolution/Community_Builds/guisettings.php?id=%s' % (url)
    link = OPEN_URL(BaseURL).replace('\n','').replace('\r','')
    guisettingsmatch = re.compile('guisettings="(.+?)"').findall(link)
    guisettingslink = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    GUI_MERGE(guisettingslink,local)
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
def GUI_MERGE(url,local):
    profiles_included=0
    keep_profiles=1
    if os.path.exists(GUINEW):
        os.remove(GUINEW)
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    if os.path.exists(PROFILES):
        os.remove(PROFILES)
    if not os.path.exists(guitemp):
        os.makedirs(guitemp)
    dp.create("Community Builds","Downloading guisettings.xml",'', 'Please Wait')
    os.rename(GUI,GUINEW) #Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    if local!=1:
        lib=os.path.join(USB, 'guifix.zip')
        downloader.download(url, lib, dp) #Download guisettings from the build
    else:
        lib=xbmc.translatePath(url)
    READ_ZIP(lib)
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,guitemp,dp)
    try:
        readfile = open(guitemp+'profiles.xml', mode='r')
        default_contents = readfile.read()
        readfile.close()
        if os.path.exists(guitemp+'profiles.xml'):
            choice = xbmcgui.Dialog().yesno("PROFILES DETECTED", 'This build has profiles included, would you like to overwrite', 'your existing profiles or keep the ones you have?', '', nolabel='Keep my profiles',yeslabel='Use new profiles')
            if choice == 0:
                pass
            elif choice == 1:
                writefile = open(PROFILES, mode='w')
                time.sleep(1)
                writefile.write(default_contents)
                time.sleep(1)
                writefile.close()
                keep_profiles=0
    except: print"no profiles.xml file"
    os.rename(guitemp+'guisettings.xml',GUIFIX) #Copy to addon_data folder so profiles can be dealt with
 # had to move elsewhere in case a profiles.xml is included  os.rename(GUI,GUIFIX) 
    time.sleep(1)
    localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
    content = file.read(localfile)
    file.close(localfile)
    skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
    skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
    skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
    skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
    lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
    lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''
    localfile2 = open(GUIFIX, mode='r')
    content2 = file.read(localfile2)
    file.close(localfile2)
    skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
    skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
    skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
    skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
    lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
    lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
    replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
    writefile = open(GUINEW, mode='w+')
    writefile.write(str(replacefile))
    writefile.close()
    if os.path.exists(GUI):
        try:
            os.remove(GUI)
            success=True
        except:
            dialog.ok("Oops we have a problem", 'There was an error trying to complete this process.', 'Please try this step again, if it still fails you may', 'need to restart Kodi and try again.')
            success=False
    try:
        os.rename(GUINEW,GUI)
        os.remove(GUIFIX)
    except:
        pass
    if success==True:
		try:
			localfile = open(tempfile, mode='r')
			content = file.read(localfile)
			file.close(localfile)
			temp = re.compile('id="(.+?)"').findall(content)
			tempcheck  = temp[0] if (len(temp) > 0) else ''
			tempname = re.compile('name="(.+?)"').findall(content)
			namecheck  = tempname[0] if (len(tempname) > 0) else ''
			tempversion = re.compile('version="(.+?)"').findall(content)
			versioncheck  = tempversion[0] if (len(tempversion) > 0) else ''
			writefile = open(idfile, mode='w+')
			writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"')
			writefile.close()
			localfile = open(startuppath, mode='r')
			content = file.read(localfile)
			file.close(localfile)
			localversionmatch = re.compile('version="(.+?)"').findall(content)
			localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
			replacefile = content.replace(localversioncheck,versioncheck)
			writefile = open(startuppath, mode='w')
			writefile.write(str(replacefile))
			writefile.close()
			os.remove(tempfile)
		except:
			writefile = open(idfile, mode='w+')
			writefile.write('id="None"\nname="Unknown"\nversion="Unknown"')
			writefile.close()                
    if os.path.exists(guitemp+'profiles.xml'):
        os.remove(guitemp+'profiles.xml')
    if keep_profiles==0:
        dialog.ok("PROFILES DETECTED", 'Unfortunately the only way to get the new profiles to stick is', 'to force close kodi. Either do this via the task manager,', 'terminal or system settings. DO NOT use the quit/exit options in Kodi.')
        killxbmc()
    else:
        if success==True:
            dialog.ok("guisettings.xml fix complete", 'Please restart Kodi. If the skin doesn\'t look', 'quite right on the next boot you may need to', 'force close Kodi.')
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
#---------------------------------------------------------------------------------------------------
#Show full description of build
def DESCRIPTION(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
    TextBoxes(buildname+'     v.'+version, '[COLOR=yellow][B]Author:   [/B][/COLOR]'+author+'[COLOR=yellow][B]               Last Updated:   [/B][/COLOR]'+updated+'[COLOR=yellow][B]               Adult Content:   [/B][/COLOR]'+adult+'[CR][CR][COLOR=yellow][B]Description:[CR][/B][/COLOR]'+description+
    '[CR][CR][COLOR=blue][B]Skins:   [/B][/COLOR]'+skins+'[CR][CR][COLOR=blue][B]Video Addons:   [/B][/COLOR]'+videoaddons+'[CR][CR][COLOR=blue][B]Audio Addons:   [/B][/COLOR]'+audioaddons+
    '[CR][CR][COLOR=blue][B]Program Addons:   [/B][/COLOR]'+programaddons+'[CR][CR][COLOR=blue][B]Picture Addons:   [/B][/COLOR]'+pictureaddons+'[CR][CR][COLOR=blue][B]Sources:   [/B][/COLOR]'+sources+
    '[CR][CR][COLOR=gold]Disclaimer: [/COLOR]These are community builds and they may overwrite some of your existing settings, '
    'things like system location and screen calibration will almost certainly have to be changed once the install has completed. TotalXBMC take no responsibility over what content '
    'is included in these builds, it\'s up to the individual who uploads the build to state what\'s included and then the users decision to decide whether or not that content is suitable for them.')
#---------------------------------------------------------------------------------------------------
#Create backup menu
def BACKUP_OPTION():
#    dialog.ok("[COLOR=red][B]VERY IMPORTANT![/COLOR][/B]", 'If you plan on creating a backup to share [COLOR=lime]ALWAYS[/COLOR] make', 'sure you\'ve deleted your addon_data folder as uninstalling', 'an addon does not remove personal data such as passwords.')             
    addDir('[COLOR=lime]Create A Commnity Build[/COLOR]','url','community_backup','Backup.png','','','Back Up Your Full System')
    addDir('Full Backup','url','backup','Backup.png','','','Back Up Your Full System')
    addDir('Backup Just Your Addons','addons','restore_zip','Backup.png','','','Back Up Your Addons')
    addDir('Backup Just Your Addon UserData','addon_data','restore_zip','Backup.png','','','Back Up Your Addon Userdata')
    addDir('Backup Guisettings.xml',GUI,'resore_backup','Backup.png','','','Back Up Your guisettings.xml')
    if os.path.exists(FAVS):
        addDir('Backup Favourites.xml',FAVS,'resore_backup','Backup.png','','','Back Up Your favourites.xml')
    if os.path.exists(SOURCE):
        addDir('Backup Source.xml',SOURCE,'resore_backup','Backup.png','','','Back Up Your sources.xml')
    if os.path.exists(ADVANCED):
        addDir('Backup Advancedsettings.xml',ADVANCED,'resore_backup','Backup.png','','','Back Up Your advancedsettings.xml')
    if os.path.exists(KEYMAPS):
        addDir('Backup Advancedsettings.xml',KEYMAPS,'resore_backup','Backup.png','','','Back Up Your keyboard.xml')
    if os.path.exists(RSS):
        addDir('Backup RssFeeds.xml',RSS,'resore_backup','Backup.png','','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
#Create restore menu
def CHECK_LOCAL_INSTALL():
    localfile = open(idfile, mode='r')
    content = file.read(localfile)
    file.close(localfile)
    localbuildmatch = re.compile('name="(.+?)"').findall(content)
    localbuildcheck  = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''
    if localbuildcheck == "Incomplete":
        choice = xbmcgui.Dialog().yesno("Finish Restore Process", 'If you\'re certain the correct skin has now been set click OK', 'to finish the install process, once complete XBMC/Kodi will', ' then close. Do you want to finish the install process?', yeslabel='Yes',nolabel='No')
        if choice == 1:
            FINISH_LOCAL_RESTORE()
        elif choice ==0:
            return
#---------------------------------------------------------------------------------------------------
def FINISH_LOCAL_RESTORE():
    os.remove(idfile)
    os.rename(idfiletemp,idfile)
    xbmc.executebuiltin('UnloadSkin')    
    xbmc.executebuiltin("ReloadSkin")
    dialog.ok("Local Restore Complete", 'XBMC/Kodi will now close.', '', '')
    xbmc.executebuiltin("Quit")      
#---------------------------------------------------------------------------------------------------
# Dialog to warn users about local guisettings fix.
def LocalGUIDialog():
    dialog.ok("Restore local guisettings fix", "You should [COLOR=lime]ONLY[/COLOR] use this option if the guisettings fix", "is failing to download via the addon. Installing via this","method will mean you do not receive any updates")
    RESTORE_LOCAL_GUI()
#---------------------------------------------------------------------------------------------------
#Create restore menu
def RESTORE_OPTION():
    CHECK_LOCAL_INSTALL()
    addDir('[COLOR=lime]RESTORE LOCAL COMMUNITY BUILD[/COLOR]','url','restore_local_CB','Restore.png','','','Back Up Your Full System')
    addDir('Restore Local guisettings fix','url','LocalGUIDialog','Restore.png','','','Back Up Your Full System')
    addDir('[COLOR=dodgerblue]FULL RESTORE[/COLOR]','url','restore','Restore.png','','','Back Up Your Full System')
    
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        addDir('Restore Your Addons','addons','restore_zip','Restore.png','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir('Restore Your Addon UserData','addon_data','restore_zip','Restore.png','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('Restore Guisettings.xml',GUI,'resore_backup','Restore.png','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('Restore Favourites.xml',FAVS,'resore_backup','Restore.png','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('Restore Source.xml',SOURCE,'resore_backup','Restore.png','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('Restore Advancedsettings.xml',ADVANCED,'resore_backup','Restore.png','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('Restore Advancedsettings.xml',KEYMAPS,'resore_backup','Restore.png','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('Restore RssFeeds.xml',RSS,'resore_backup','Restore.png','','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
#Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
def RESTORE_ZIP_FILE(url):
    CHECK_DOWNLOAD_PATH()
    if 'addons' in url:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR = ADDONS
        to_backup = ADDONS
        
        backup_zip = xbmc.translatePath(os.path.join(USB,'addons.zip'))
    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA
        
    if 'Backup' in name:
        DeletePackages() 
        import zipfile
        import sys
        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Backing Up",'', 'Please Wait')
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not 'plugin.program.community.builds' in dirs:
                       import time
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]", "You Are Now Backed Up", '','')   
    else:

        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
        
        import time
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(ZIPFILE,DIR,dp)
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        
        if 'Backup' in name:
            killxbmc()
            dialog.ok("Community Builds - Install Complete", 'To ensure the skin settings are set correctly XBMC will now', 'close. If XBMC doesn\'t close please force close (pull power', 'or force close in your OS - [COLOR=lime]DO NOT exit via XBMC menu[/COLOR])')
        else:
            dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]", "You Are Now Restored", '','')        
#---------------------------------------------------------------------------------------------------
#Function to restore a backup xml file (guisettings, sources, RSS)
def RESTORE_BACKUP_XML(name,url,description):
    if 'Backup' in name:
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        
        f = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
         
    else:
    
        if 'guisettings.xml' in description:
            a = open(os.path.join(USB,description.split('Your ')[1])).read()
            
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            
            match=re.compile(r).findall(a)
            print match
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        else:    
            TO_WRITE   = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            
            f = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  
    dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]", "", 'All Done !','')
#---------------------------------------------------------------------------------------------------
#Function to delete the packages folder
def DeletePackages():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
 
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        
    # Count files and give option to delete
        if file_count > 0:
                        
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#---------------------------------------------------------------------------------------------------
#Function to delete the userdata/addon_data folder
def DeleteUserData():
    print '############################################################       DELETING USERDATA             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
 
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        
    # Count files and give option to delete
        if file_count > 0:
                        
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#---------------------------------------------------------------------------------------------------
#Function to do a full wipe. Thanks to kozz for working out how to add an exclude clause so community builds addon_data and addon isn't touched.
def WipeXBMC():
    if skin!= "skin.confluence":
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    else:
        choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'This will completely wipe your install.', 'Would you like to create a backup before proceeding?', '', yeslabel='Yes',nolabel='No')
        if choice == 1:
            BACKUP()
        choice = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe this install?', '', 'All addons and settings will be completely wiped!', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
            dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Wiping Install",'', 'Please Wait')
            try:
                for root, dirs, files in os.walk(HOME,topdown=True):
                    dirs[:] = [d for d in dirs if d not in EXCLUDES]
                    for name in files:
                        try:
                            os.remove(os.path.join(root,name))
                            os.rmdir(os.path.join(root,name))
                        except: pass
                            
                    for name in dirs:
                        try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                        except: pass
 #               if not failed:
 #                   print"community.builds.WipeXBMC All user files removed, you now have a clean install"
 #                   dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Wipe Successful, please restart XBMC/Kodi for changes to take effect.','','')
 #               else:
 #                   print"community.builds.WipeXBMC User files partially removed"
 #                   dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Wipe Successful, please restart XBMC/Kodi for changes to take effect.','','')
            except: pass
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Wipe Successful, please restart XBMC/Kodi for changes to take effect.','','')

#---------------------------------------------------------------------------------------------------
#Function to do remove all empty folders after delete       
def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count
#---------------------------------------------------------------------------------------------------
#Function to do a full wipe - this is called when doing a fresh CB install.
#Thanks to kozz for working out how to add an exclude clause so community builds addon_data and addon isn't touched.
def WipeInstall():
    if skin!= "skin.confluence":
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")       
    else:
        choice = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe this install?', '', 'All addons and settings will be completely wiped!', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
            dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Wiping Install",'', 'Please Wait')
            addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
            xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("community.builds.WipeXBMC xbmcPath="+xbmcPath); failed=False  
            try:
                for root, dirs, files in os.walk(xbmcPath,topdown=True):
                    dirs[:] = [d for d in dirs if d not in EXCLUDES]
                    for name in files:
                        try: os.remove(os.path.join(root,name))
                        except: pass
                    for name in dirs:
                        try: os.rmdir(os.path.join(root,name))
                        except: pass
            except: pass
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
#---------------------------------------------------------------------------------------------------
#Get params and clean up into string or integer
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
#---------------------------------------------------------------------------------------------------
#Main addDirectory function - xbmcplugin.addDirectoryItem()
def addDirectoryItem(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
#---------------------------------------------------------------------------------------------------
#Add a standard directory and grab fanart and iconimage from artpath defined in global variables
def addDir(name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
    if len(iconimage) > 0:
        iconimage = ARTPATH + iconimage
    else:
        iconimage = 'DefaultFolder.png'
        
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    if (mode==None) or (mode=='Search_Private') or (mode=='additional_tools') or (mode=='search_builds') or (mode=='manual_search') or (mode=='genres2') or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='grab_builds2') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries')or (url==None) or (len(url)<1):
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
#---------------------------------------------------------------------------------------------------
def addDir2(name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
    if len(iconimage) > 0:
        iconimage = ARTPATH + iconimage
    else:
        iconimage = 'DefaultFolder.png'
        
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
#---------------------------------------------------------------------------------------------------
#Add a standard directory for the builds. Essentially the same as above but grabs unique artwork from previous call
def addBuildDir(name,url,mode,iconimage,fanart,video,description,skins,guisettingslink):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)+"&skins="+urllib.quote_plus(skins)+"&guisettingslink="+urllib.quote_plus(guisettingslink)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        if (mode==None) or (mode=='genres2') or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='grab_builds2') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries')or (url==None) or (len(url)<1):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
#---------------------------------------------------------------------------------------------------
#Add a directory for the description, this requires multiple string to be called from previous menu
def addDescDir(name,url,mode,iconimage,fanart,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
        iconimage = ARTPATH + iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&author="+urllib.quote_plus(author)+"&description="+urllib.quote_plus(description)+"&version="+urllib.quote_plus(version)+"&buildname="+urllib.quote_plus(buildname)+"&updated="+urllib.quote_plus(updated)+"&skins="+urllib.quote_plus(skins)+"&videoaddons="+urllib.quote_plus(videoaddons)+"&audioaddons="+urllib.quote_plus(audioaddons)+"&buildname="+urllib.quote_plus(buildname)+"&programaddons="+urllib.quote_plus(programaddons)+"&pictureaddons="+urllib.quote_plus(pictureaddons)+"&sources="+urllib.quote_plus(sources)+"&adult="+urllib.quote_plus(adult)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
#---------------------------------------------------------------------------------------------------
#Function to return the platform XBMC is currently running on.
#Could possibly do away with this and use xbmc.getInfoLabel("System.BuildVersion") in the killxbmc function
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
#---------------------------------------------------------------------------------------------------
# Addon starts here
params=get_params()
url=None
name=None
buildname=None
updated=None
author=None
version=None
mode=None
iconimage=None
description=None
video=None
link=None
skins=None
videoaddons=None
audioaddons=None
programaddons=None
audioaddons=None
sources=None
local=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        mode=str(params["mode"])
except:
        pass
try:
        link=urllib.unquote_plus(params["link"])
except:
        pass
try:
        skins=urllib.unquote_plus(params["skins"])
except:
        pass
try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
except:
        pass
try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
except:
        pass
try:
        programaddons=urllib.unquote_plus(params["programaddons"])
except:
        pass
try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except:
        pass
try:
        local=urllib.unquote_plus(params["local"])
except:
        pass
try:
        sources=urllib.unquote_plus(params["sources"])
except:
        pass
try:
        adult=urllib.unquote_plus(params["adult"])
except:
        pass
try:
        buildname=urllib.unquote_plus(params["buildname"])
except:
        pass
try:
        updated=urllib.unquote_plus(params["updated"])
except:
        pass
try:
        version=urllib.unquote_plus(params["version"])
except:
        pass
try:
        author=urllib.unquote_plus(params["author"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        video=urllib.unquote_plus(params["video"])
except:
        pass

        
if mode==None or url==None or len(url)<1:
        VideoCheck()
elif mode=='backup_option':
        BACKUP_OPTION()
elif mode=='restore':
        print "############   RESTORE  #################"
        RESTORE()    
elif mode=='additional_tools':
        print "############   ADDITIONAL TOOLS  #################"
        ADDITIONAL_TOOLS()   
elif mode=='community_backup':
        print "############   COMMUNITY BACKUP  #################"
        COMMUNITY_BACKUP()
elif mode=='backup':
        print "############   BACKUP  #################"
        BACKUP()
elif mode=='restore_backup':
        print "############   RESTORE_BACKUP_XML #################"
        RESTORE_BACKUP_XML(name,url,description)
elif mode=='restore_option':
        print "############   RESTORE_OPTION   #################"
        RESTORE_OPTION()
elif mode=='restore_zip':
        print "############   RESTORE_ZIP_FILE   #################"
        RESTORE_ZIP_FILE(url)         
elif mode=='restore_community':
        print "############   RESTORE_COMMUNITY BUILD  #################"
        RESTORE_COMMUNITY(name,url,description,skins,guisettingslink)        
elif mode=='grab_builds2':
        print "############   CALL COMMUNITY SECTION   #################"
        COMMUNITY2(url)        
elif mode=='wipe_xbmc':
        print "############   WIPE XBMC   #################"
        WipeXBMC()
elif mode=='description':
        print "############   BUILD DESCRIPTION   #################"
        DESCRIPTION(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
elif mode=='community_menu':
        print "############   BUILD COMMUNITY LIST   #################"
        COMMUNITY_MENU(url)        
elif mode=='play_video':
        print "############   PLAY VIDEO   #################"
        PLAYVIDEO(url)
elif mode=='instructions':
        print "############   INSTRUCTIONS MENU   #################"
        INSTRUCTIONS(url)
elif mode=='instructions_1':
        print "############   SHOW INSTRUCTIONS 1   #################"
        Instructions_1()
elif mode=='instructions_2':
        print "############   SHOW INSTRUCTIONS 2   #################"
        Instructions_2()
elif mode=='instructions_3':
        print "############   SHOW INSTRUCTIONS 3   #################"
        Instructions_3()
elif mode=='instructions_4':
        print "############   SHOW INSTRUCTIONS 4   #################"
        Instructions_4()
elif mode=='instructions_5':
        print "############   SHOW INSTRUCTIONS 5   #################"
        Instructions_5()
elif mode=='instructions_6':
        print "############   SHOW INSTRUCTIONS 6   #################"
        Instructions_6()
elif mode=='cb_root_menu':
        print "############   Community Builds Menu   #################"
        CB_Root_Menu()
elif mode=='genres':
        print "############   Build GENRE1 Menu   #################"
        GENRES()
elif mode=='countries':
        print "############   Build COUNTRIES Menu   #################"
        COUNTRIES()
elif mode=='genres2':
        print "############   Build GENRE2 Menu   #################"
        GENRES2(url)
elif mode=='search_builds':
        print "############   MANUAL SEARCH BUILDS   #################"
        SEARCH_BUILDS()
elif mode=='manual_search':
        print "############   MANUAL SEARCH BUILDS   #################"
        MANUAL_SEARCH()
elif mode=='grab_builds':
        print "############   MANUAL SEARCH BUILDS   #################"
        grab_builds(url)
elif mode=='guisettingsfix':
        print "############   GUISETTINGS FIX   #################"
        GUISETTINGS_FIX(url,local)
elif mode=='showinfo':
        print "############   SHOW BASIC BUILD INFO   #################"
        SHOWINFO(url)
elif mode=='remove_build':
        print "############   SHOW BASIC BUILD INFO   #################"
        REMOVE_BUILD()
elif mode=='kill_xbmc':
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        killxbmc()
elif mode=='fix_special':
        print "############   FIX SPECIAL PATHS   #################"
        FIX_SPECIAL(url)
elif mode=='restore_local_CB':
        print "############   FIX SPECIAL PATHS   #################"
        RESTORE_LOCAL_COMMUNITY()
elif mode=='restore_local_gui':
        print "############   FIX SPECIAL PATHS   #################"
        RESTORE_LOCAL_GUI()
elif mode=='Addon_Settings':
        print "############   Open Addon Settings   #################"
        Addon_Settings()
elif mode=='Register':
        print "############   Open Register dialog   #################"
        Register()
elif mode=='LocalGUIDialog':
        print "############   Open Local GUI dialog   #################"
        LocalGUIDialog()
elif mode=='Search_Private':
        print "############   Private search   #################"
        PRIVATE_SEARCH(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))