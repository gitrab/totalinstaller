import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools

ADDON        =  xbmcaddon.Addon(id='plugin.program.community.builds')
AddonID      =  'plugin.program.community.builds'
AddonTitle   =  "[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]"
zip          =  ADDON.getSetting('zip')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons'))
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
skin         =  xbmc.getSkinDir()


#-----------------------------------------------------------------------------------------------------------------    
            
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

def BACKUP():  
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    to_backup = xbmc.translatePath(os.path.join('special://','home'))
    backup_zip = xbmc.translatePath(os.path.join(USB,'backup.zip'))
    DeletePackages()    
    choice = xbmcgui.Dialog().yesno('WARNING', 'If you intend on sharing this backup it\'s highly', 'recommended to delete your addon_data folder as it can', 'contain personal login info.', nolabel='DO NOT Delete Data',yeslabel='[COLOR=red]YES, Delete Data[/COLOR]')
    if choice == 1:
        choice2 = xbmcgui.Dialog().yesno('Absolutely sure?!', 'Are you [COLOR=lime]ABSOLUTELY[/COLOR] sure you want to delete this folder?', 'This contains all your addon settings, once it\'s gone there\'s', 'no getting it back!', nolabel='NO, take me back!',yeslabel='Continue, I understand')
        if choice2 == 1:
            DeleteUserData()
        else:
            return
    import zipfile
    
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Backing Up",'', 'Please Wait')
    zipobj = zipfile.ZipFile(backup_zip , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(to_backup)
    for_progress = []
    ITEM =[]
    for base, dirs, files in os.walk(to_backup):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(to_backup):
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
    dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] Community Builds[/B]", 'You Are Now Backed Up. If you\'d like to share this build with', 'the community please post details on the forum at', '[COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')
    
#---------------------------------------------------------------------------------------------------
      
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

def COMMUNITY():
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your backup storage folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    link = OPEN_URL('http://totalxbmc.tv/totalrevolution/Community_Builds/community_builds.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"video="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,video,description in match:
        addDir(name,url,11,iconimage,fanart,video,description)
    
#---------------------------------------------------------------------------------------------------

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

#---------------------------------------------------------------------------------------------------

def RESTORE_COMMUNITY(name,url,description):
    import time
    myplatform = platform()
    dialog = xbmcgui.Dialog()
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before', 'installing any community builds.', 'Are you sure you want to install this build?', nolabel='Cancel',yeslabel='Install')
    if choice == 0:
        return
    elif choice == 1:
        if myplatform != 'android':
            choice2 = xbmcgui.Dialog().yesno(name, 'Would you like to merge your existing build', 'or wipe your existing data and have a fresh', 'install with this new build?', nolabel='Merge',yeslabel='Wipe')
            if choice2 == 0: pass
            elif choice2 == 1: WipeInstall()
#        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        dp = xbmcgui.DialogProgress()
        dp.create("Community Builds","Downloading "+name +" build.",'', 'Please Wait')
        lib=os.path.join(zip, 'community.zip')
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, dp)
        READ_ZIP(lib)
        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
        HOME = xbmc.translatePath(os.path.join('special://','home')) 
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(lib,HOME,dp)
        time.sleep(1)
        dialog.ok("Community Builds - Install Complete", 'To ensure the skin settings are set correctly XBMC will now', 'close. If XBMC doesn\'t close please force close (pull power', 'or force close in your OS - [COLOR=lime]DO NOT exit via XBMC menu[/COLOR])')
        killxbmc()
#---------------------------------------------------------------------------------------------------
        
def RESTORE():
    import time
    dialog = xbmcgui.Dialog()
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
        
    lib=xbmc.translatePath(os.path.join(zip,'backup.zip'))
    READ_ZIP(lib)
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
    HOME = xbmc.translatePath(os.path.join('special://','home'))
    
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,HOME,dp)
    time.sleep(1)
    dialog.ok("Community Builds - Install Complete", 'To ensure the skin settings are set correctly XBMC will now', 'close. If XBMC doesn\'t close please force close (pull power', 'or force close in your OS - [COLOR=lime]DO NOT exit via XBMC menu[/COLOR])')
    killxbmc()
#---------------------------------------------------------------------------------------------------
        
# Kill Commands - these will make sure guisettings.xml sticks
def killxbmc():
    myplatform = platform()
    print "Platform: " + str(myplatform)
#OSX
    if myplatform == 'osx':
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]W A R N I N G   ! ! ![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.",'')        
#Linux
    elif myplatform == 'linux':
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 Kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]W A R N I N G   ! ! ![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.",'')        
# Android       
    elif myplatform == 'android':
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.Kodi.Kodi')
        except: pass
        try: os.system('adb shell am force-stop org.Kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]W A R N I N G   ! ! ![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your system has been detected as Android, just pull the power cable.")
# Windows
    elif myplatform == 'windows':
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
        dialog.ok("[COLOR=red][B]W A R N I N G   ! ! ![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your system has been detected as Windows so use ALT + F4.")

# Possible alternative for older builds - windows tskill XBMC.exe
#ATV
    else:
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
#OSMC / Raspbmc
        print "############   try raspbmc force close  #################"
        try: os.system('sudo initctl stop Kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]W A R N I N G   ! ! ![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")
        
#---------------------------------------------------------------------------------------------------
    
    
def CATEGORIES():
    addDir('[COLOR=dodgerblue]How To Use This Addon[/COLOR]','url',13,'','','','Instructions')
    addDir('[COLOR=lime]Install Community Build[/COLOR]','url',8,'','','','Install Community Build')
    addDir('Backup My Content','url',1,'','','','Back Up Your Data')
    addDir('Restore My Content','url',5,'','','','Restore Your Data')
    addDir('Wipe My Setup (Fresh Start)','url',9,'','','','Wipe your special XBMC/Kodi directory which will revert back to a vanillla build.')

#---------------------------------------------------------------------------------------------------
def PLAYVIDEO(url):
    import yt    
    yt.PlayVideo(url)
    
#---------------------------------------------------------------------------------------------------

def INSTRUCTIONS(url):
    addDir('[COLOR=dodgerblue][TEXT GUIDE][/COLOR] What Is Community Builds?','url',16,'','','','')
    addDir('[COLOR=dodgerblue][TEXT GUIDE][/COLOR] Creating A Community Build','url',14,'','','','')
    addDir('[COLOR=dodgerblue][TEXT GUIDE][/COLOR] Installing A Community Build','url',15,'','','','')
#    addDir('[COLOR=lime][VIDEO GUIDE][/COLOR] Create a Community Build (part 1)','url','PLAYVIDEO(https://www.youtube.com/watch?v=3rMScZF2h_U)','','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Submitting A Community Backup[/COLOR]','url',16,'','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Creating A Local Backup[/COLOR]','url',17,'','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Restoring A Local Backup[/COLOR]','url',18,'','','','')
#    addDir('[COLOR=dodgerblue][TEXT GUIDE] Fresh Start XBMC/Kodi[/COLOR]','url',19,'','','','')
#    addDirvid('Watch preview video','url','plugin://plugin.video.youtube/?action=play_video&videoid='+video,'','','',description)

def Instructions_1():
    TextBoxes('Creating A Community Backup', '[COLOR=blue][B]Step 1: Backup your system[/B][/COLOR][CR]Choose the backup option from the main menu, you will be asked whether you would like to delete your addon_data folder. If you decide to choose this option [COLOR=yellow][B]make sure[/COLOR][/B] you already have a full backup of your system as it will completely wipe your addon settings (any stored settings such as passwords or any other changes you\'ve made to addons since they were first installed). If sharing a build with the community it\'s highly advised that you wipe your addon_data but if you\'ve made changes or installed extra data packages (e.g. skin artwork packs) then backup the whole build and then manually delete these on your PC and zip back up again (more on this later).'
    '[CR][CR][COLOR=blue][B]Step 2: Edit zip file on your PC[/B][/COLOR][CR]Copy your backup.zip file to your PC, extract it and delete all the addons and addon_data that isn\'t required.'
    '[CR][COLOR=blue]What to delete:[/COLOR][CR][COLOR=lime]/addons/packages[/COLOR] This folder contains zip files of EVERY addon you\'ve ever installed - it\'s not needed.'
    '[CR][COLOR=lime]/addons/<skin.xxx>[/COLOR] Delete any skins that aren\'t used, these can be very big files.'
    '[CR][COLOR=lime]/addons/<addon_id>[/COLOR] Delete any other addons that aren\'t used, it\'s easy to forget you\'ve got things installed that are no longer needed.'
    '[CR][COLOR=lime]/userdata/addon_data/<addon_id>[/COLOR] Delete any folders that don\'t contain important changes to addons. If you delete these the associated addons will just reset to their default values.'
    '[CR][COLOR=lime]/userdata/<all other folders>[/COLOR] Delete all other folders in here such as keymaps. If you\'ve setup profiles make sure you [COLOR=yellow][B]keep the profiles directory[/COLOR][/B].'
    '[CR][COLOR=lime]/userdata/Thumbnails/[/COLOR] Delete this folder, it contains all cached artwork. You can safely delete this but must also delete the file listed below.'
    '[CR][COLOR=lime]/userdata/Database/textures13.db[/COLOR] Delete this and it will tell XBMC to regenerate your thumbnails - must do this if delting thumbnails folder.'
    '[CR][COLOR=lime]/xbmc.log (or Kodi.log)[/COLOR] Delete your log files, this includes any crashlog files you may have.'
    '[CR][CR][COLOR=blue][B]Step 3: Compress and upload[/B][/COLOR][CR]Use a program like 7zip to create a zip file of your remaining folders and upload to a file sharing site like dropbox.'
    '[CR][CR][COLOR=blue][B]Step 4: Submit build at TotalXBMC[/B][/COLOR]'
    '[CR]Create a thread on the Community Builds section of the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B].[CR]Full details can be found on there of the template you should use when posting.')
    
def Instructions_2():
    TextBoxes('Installing a community build', '[COLOR=blue][B]Step 1 (Optional): Backup your system[/B][/COLOR][CR]We highly recommend creating a backup of your system in case you don\'t like the build and want to revert back. Choose the backup option from the main menu, you will be asked whether you would like to delete your addon_data folder, select no unless you want to lose all your settings. If you ever need your backup it\'s stored in the location you\'ve selected in the addon settings.'
    '[CR][CR][COLOR=blue][B]Step 2: Browse the Community Builds[/B][/COLOR][CR]Find a community build you like the look of and make sure you read the description as it could contain unsuitable content or have specific install instructions. Once you\'ve found the build you want to install click on the install option and you\'ll have the option of a fresh install or a merge [COLOR=yellow](on android fresh instlall is not possible so it will automatically merge)[/COLOR]. The merge option will leave all your existing addons and userdata in place and just add the contents of the new build whereas the fresh (wipe) option will completely wipe your existing data and replace with content on the new build. Once you make your choice the download and extraction process will begin.'
    '[CR][CR][COLOR=blue][B]Step 3: [/COLOR][COLOR=red]VERY IMPORTANT[/COLOR][COLOR=blue] Force Close XBMC/Kodi[/B][/COLOR][CR]For the install to complete properly you MUST force close XBMC/Kodi, if you exit XBMC cleanly the skin settings will not take effect and you\'ll end up with some sort of hybrid build not quite finished! The addon will attempt to force close but if it doesn\'t the easiest option is to just pull the power to your device unless you know how to force close XBMC/Kodi (e.g. on Windows it would be ALT + F4).'
    '[CR][CR][COLOR=blue][B]Step 4: Load XBMC/Kodi[/B][/COLOR][CR]You can now safely load up XBMC/Kodi and all changes should have taken effect')

def Instructions_3():
    TextBoxes('What is a community build', 'Community Builds are pre-configured builds of XBMC/Kodi based on different users setups. Have you ever watched youtube videos or seen screenshots of Kodi in action and thought "wow I wish I could do that"? Well now you can have a brilliant setup at the click of a button, completely pre-configured by users on the [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B] forum. If you\'d like to get involved yourself and share your build with the community it\'s very simple to do, just go to the forum where you\'ll find full details or you can follow the guide in this addon.')
 
def Instructions_4():
    TextBoxes('Creating A Community Backup', '[COLOR=blue][B]Step 1: Backup your system[/B][CR]Choose the backup option from the main manu, you will be asked whether you would like to delete your addon_data folder. If you decide to choose this option [COLOR=yellow}[B]make sure[/COLOR][/B] you already have a full backup of your system as it will completely wipe your addon settings (any stored settings such as passwords or any other changes you\'ve made to addons since they were first installed).')

def Instructions_5():
    TextBoxes('Creating A Community Backup', '[COLOR=blue][B]Step 1: Backup your system[/B][CR]Choose the backup option from the main manu, you will be asked whether you would like to delete your addon_data folder. If you decide to choose this option [COLOR=yellow}[B]make sure[/COLOR][/B] you already have a full backup of your system as it will completely wipe your addon settings (any stored settings such as passwords or any other changes you\'ve made to addons since they were first installed).')

def Instructions_6():
    TextBoxes('Creating A Community Backup', '[COLOR=blue][B]Step 1: Backup your system[/B][CR]Choose the backup option from the main manu, you will be asked whether you would like to delete your addon_data folder. If you decide to choose this option [COLOR=yellow}[B]make sure[/COLOR][/B] you already have a full backup of your system as it will completely wipe your addon settings (any stored settings such as passwords or any other changes you\'ve made to addons since they were first installed).')
#---------------------------------------------------------------------------------------------------

def COMMUNITY_MENU(name,url,description,video):
    addDir('Full description','url',10,'','','',description)
# NOT WORKING, DON'T KNOW WHY    addDirVid('Watch preview video',video,12,'','','',description)
    addDir('Install '+name+' Build',url,7,'','','',description)
    
#---------------------------------------------------------------------------------------------------

def DESCRIPTION(name,url,description):
    TextBoxes(name, '[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] Community Builds[/B][CR]These are community builds and they may overwrite some of your existing settings, things like system location and screen calibration will almost certainly have to be changed once the install has completed. TotalXBMC take no responsibility over what content is included in these builds, it\'s up to the individual who uploads the build to state what\'s included and then the users decision to decide whether or not that content is suitable for them.[CR][CR][CR][COLOR=yellow][B]Description:[CR][/B][/COLOR]'+description)

#---------------------------------------------------------------------------------------------------

def BACKUP_OPTION():
    dialog.ok("[COLOR=red][B]VERY IMPORTANT![/COLOR][/B]", 'If you plan on creating a backup to share [COLOR=lime]ALWAYS[/COLOR] make', 'sure you\'ve deleted your addon_data folder as uninstalling', 'an addon does not remove personal data such as passwords.')             
    addDir('FULL BACKUP','url',3,'','','','Back Up Your Full System')
    addDir('Backup Just Your Addons','addons',6,'','','','Back Up Your Addons')
    addDir('Backup Just Your Addon UserData','addon_data',6,'','','','Back Up Your Addon Userdata')
    addDir('Backup Guisettings.xml',GUI,4,'','','','Back Up Your guisettings.xml')
    if os.path.exists(FAVS):
        addDir('Backup Favourites.xml',FAVS,4,'','','','Back Up Your favourites.xml')
    if os.path.exists(SOURCE):
        addDir('Backup Source.xml',SOURCE,4,'','','','Back Up Your sources.xml')
    if os.path.exists(ADVANCED):
        addDir('Backup Advancedsettings.xml',ADVANCED,4,'','','','Back Up Your advancedsettings.xml')
    if os.path.exists(KEYMAPS):
        addDir('Backup Advancedsettings.xml',KEYMAPS,4,'','','','Back Up Your keyboard.xml')
    if os.path.exists(RSS):
        addDir('Backup RssFeeds.xml',RSS,4,'','','','Back Up Your RssFeeds.xml')    

#---------------------------------------------------------------------------------------------------

def RESTORE_OPTION():
    if os.path.exists(os.path.join(USB,'backup.zip')):   
        addDir('FULL RESTORE','url',2,'','','','Back Up Your Full System')
        
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        addDir('Restore Your Addons','addons',6,'','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir('Restore Your Addon UserData','addon_data',6,'','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('Restore Guisettings.xml',GUI,4,'','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('Restore Favourites.xml',FAVS,4,'','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('Restore Source.xml',SOURCE,4,'','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('Restore Advancedsettings.xml',ADVANCED,4,'','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('Restore Advancedsettings.xml',KEYMAPS,4,'','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('Restore RssFeeds.xml',RSS,4,'','','','Restore Your RssFeeds.xml')    

#---------------------------------------------------------------------------------------------------

def RESTORE_ZIP_FILE(url):
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
        
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

def WipeXBMC():
    plugintools.log("community.builds.WipeXBMC "+repr(params)); yes_pressed=plugintools.message_yes_no(AddonTitle,"This will completely wipe your existing setup.","Are you [COLOR=lime]ABSOSLUTELY[/COLOR] certain you wish to proceed?")
    if yes_pressed:
        addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
        xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("community.builds.WipeXBMC xbmcPath="+xbmcPath); failed=False  
        try:
            for root, dirs, files in os.walk(xbmcPath,topdown=False):
                for name in files:
                    try: os.remove(os.path.join(root,name))
                    except:
                        if name not in ["Addons15.db","Addons16.db","MyVideos75.db","MyVideos78.db","MyVideos90.db","Textures13.db","xbmc.log","kodi.log"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name))
                    except:
                        if name not in ["Database","userdata"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
            if not failed: plugintools.log("community.builds.WipeXBMC All user files removed, you now have a clean install"); plugintools.message(AddonTitle,"Wipe complete, you now have a fresh install.","The addon will now attempt to close XBMC/Kodi."); xbmc.executebuiltin("RestartApp")
            else: plugintools.log("community.builds.WipeXBMC User files partially removed"); plugintools.message(AddonTitle,"Wipe complete, you now have a fresh install.","The addon will now attempt to close XBMC/Kodi."); xbmc.executebuiltin("RestartApp")
        except: plugintools.message(AddonTitle,"Problem found","Your settings has not been changed"); import traceback; plugintools.log(traceback.format_exc()); plugintools.log("community.builds.WipeXBMC NOT removed")
        plugintools.add_item(action="",title="Done",folder=False)
    else: plugintools.message(AddonTitle,"Your settings","has not been changed"); plugintools.add_item(action="",title="Done",folder=False)
    
#---------------------------------------------------------------------------------------------------

def WipeInstall():
    plugintools.log("community.builds.WipeXBMC "+repr(params)); yes_pressed=plugintools.message_yes_no(AddonTitle,"This will completely wipe your existing setup.","Are you [COLOR=lime]ABSOSLUTELY[/COLOR] certain you wish to proceed?")
    if yes_pressed:
        addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
        xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("community.builds.WipeXBMC xbmcPath="+xbmcPath); failed=False  
        try:
            for root, dirs, files in os.walk(xbmcPath,topdown=False):
                for name in files:
                    try: os.remove(os.path.join(root,name))
                    except:
                        if name not in ["Addons*.db","MyVideos*.db","Textures*.db","xbmc.log","kodi.log"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name))
                    except:
                        if name not in ["Database","userdata"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
        except: pass
    else: return
#---------------------------------------------------------------------------------------------------

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

def addDir(name,url,mode,iconimage,fanart,video,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        if (mode==None) or (mode==5) or (mode==1) or (mode==6) or (mode==8) or (mode==11) or (mode==13) or (url==None) or (len(url)<1):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDirvid(name,url,mode,iconimage,fanart,video,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Addon.Video", video )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)

#---------------------------------------------------------------------------------------------------
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
   
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
video=None

try:
        url=urllib.unquote_plus(params["url"])
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
        mode=int(params["mode"])
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
        CATEGORIES()
elif mode==1:
        BACKUP_OPTION()
elif mode==2:
        print "############   RESTORE  #################"
        RESTORE()    
elif mode==3:
        print "############   BACKUP  #################"
        BACKUP()
elif mode==4:
        print "############   RESTORE_BACKUP_XML #################"
        RESTORE_BACKUP_XML(name,url,description)
elif mode==5:
        print "############   RESTORE_OPTION   #################"
        RESTORE_OPTION()
elif mode==6:
        print "############   RESTORE_ZIP_FILE   #################"
        RESTORE_ZIP_FILE(url)         
elif mode==7:
        print "############   RESTORE_COMMUNITY BUILD  #################"
        RESTORE_COMMUNITY(name,url,description)        
elif mode==8:
        print "############   CALL COMMUNITY SECTION   #################"
        COMMUNITY()        
elif mode==9:
        print "############   WIPE XBMC   #################"
        WipeXBMC()
elif mode==10:
        print "############   BUILD DESCRIPTION   #################"
        DESCRIPTION(name,url,description)        
elif mode==11:
        print "############   BUILD DESCRIPTION   #################"
        COMMUNITY_MENU(name,url,description,video)        
elif mode==12:
        print "############   PLAY VIDEO   #################"
        PLAYVIDEO(url)
elif mode==13:
        print "############   INSTRUCTIONS MENU   #################"
        INSTRUCTIONS(url)
elif mode==14:
        print "############   SHOW INSTRUCTIONS 1   #################"
        Instructions_1()
elif mode==15:
        print "############   SHOW INSTRUCTIONS 2   #################"
        Instructions_2()
elif mode==16:
        print "############   SHOW INSTRUCTIONS 3   #################"
        Instructions_3()
elif mode==17:
        print "############   SHOW INSTRUCTIONS 4   #################"
        Instructions_4()
elif mode==18:
        print "############   SHOW INSTRUCTIONS 5   #################"
        Instructions_5()
elif mode==19:
        print "############   SHOW INSTRUCTIONS 6   #################"
        Instructions_6()

xbmcplugin.endOfDirectory(int(sys.argv[1]))