
from pygame import image, Surface, Rect
from os.path import join


class FrameManager(object):
   """A singleton factory class to create and store frames on demand."""

   # The singleton instance variable
   _INSTANCE = None

   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._FM()

      return cls._INSTANCE

   # Do not directly instantiate this class!
   class _FM(object):
      """An internal FrameManager class to contain the actual code. Is a private class."""

      # Folder in which images are stored
      _IMAGE_FOLDER = "images"

      # Static information about the frame sizes of particular image sheets.
      _FRAME_SIZES = {
         "blobs.png" : (32,32),
         "bra.png": (32,32),
         "weddingring.png": (32,32),
         "platform.png": (52,10),
         "water-lilly.png" : (47,49),
         "background.png": (2400, 400),
         "ground2.png": (2400, 100),
         "flowers.png": (16,16),
         "nuts_and_milk.png": (16,16),
         "dizzy_devil.png": (32,32),
         "elevator_back.png": (50,20),
         "elevator_doors.png": (50,20),
         "elevator_front.png": (50,20),
         "elevator_top.png": (50,10),
         "bubble_enemies.png": (21,19),
         "gaston.png": (30,40),
      }

      # A default frame size
      _DEFAULT_FRAME = (32,32)

      # A list of images that require to be loaded with transparency
      _TRANSPARENCY = []

      # A list of images that require to be loaded with a color key
      _COLOR_KEY = ["blobs.png", "fryingpan.png", "bra.png", "weddingring.png", "platform.png", "flowers.png", "nuts_and_milk.png", "dizzy_devil.png", "bubble_enemies.png", "gaston.png"]



      def __init__(self):
         # Stores the surfaces indexed based on file name
         # The values in _surfaces can be a single Surface
         #  or a two dimentional grid of surfaces if it is an image sheet
         self._surfaces = {}


      def __getitem__(self, key):
         return self._surfaces[key]

      def __setitem__(self, key, item):
         self._surfaces[key] = item


      def getFrame(self, fileName, offset=None):
         # If this frame has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset != None)

         # If this is an image sheet, return the correctly offset sub surface
         if offset != None:
            return self[fileName][offset[1]][offset[0]]

         # Otherwise, return the sheet created
         return self[fileName]

      def _loadImage(self, fileName, sheet=False):
         # Load the full image
         fullImage = image.load(join(FrameManager._FM._IMAGE_FOLDER, fileName))

         # Look up some information about the image to be loaded
         transparent = fileName in FrameManager._FM._TRANSPARENCY
         colorKey = fileName in FrameManager._FM._COLOR_KEY

         # Detect if a transparency is needed
         if transparent:
            fullImage = fullImage.convert_alpha()
         else:
            fullImage = fullImage.convert()

         # If the image to be loaded is an image sheet, split it up based on the frame size
         if sheet:

            self[fileName] = []
            spriteSize = FrameManager._FM._FRAME_SIZES.get(fileName, FrameManager._FM._DEFAULT_FRAME)

            sheetDimensions = fullImage.get_size()

            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               for x in range(0, sheetDimensions[0], spriteSize[0]):

                  # If we need transparency
                  if transparent:
                     frame = Surface(spriteSize, pygame.SRCALPHA, 32)
                  else:
                     frame = Surface(spriteSize)

                  frame.blit(fullImage, (0,0), Rect((x,y), spriteSize))

                  # If we need to set the color key
                  if colorKey:
                     frame.set_colorkey(frame.get_at((0,0)))

                  self[fileName][-1].append(frame)
         else:

            self[fileName] = fullImage

            # If we need to set the color key
            if colorKey:
               self[fileName].set_colorkey(self[fileName].get_at((0,0)))

# Set up an instance for others to import
FRAMES = FrameManager.getInstance()
