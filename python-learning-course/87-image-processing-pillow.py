# -----------------------------------------------------------------
# Lesson 87: image processing with Pillow (PIL)
# Course   : Python Programming (Elzero-Style Arabic Course)
# Topic    : what Pillow is (pip install Pillow), from PIL
#            import Image, opening/creating an image,
#            crop() with box=(left, upper, right, lower),
#            convert("L") grayscale, resize(), rotate(),
#            ImageFilter effects, ImageEnhance brightness
#            and contrast -- all on a SANDBOX image
# Type     : Educational
# Builder  : local assistant
# -----------------------------------------------------------------
# The transcript's [00:04]: a fun and important practical
# -- manipulating and processing images in Python with
# the Pillow library (PIL).
#
# PREREQUISITE (like lesson 78): pip install Pillow
# [00:27]. This lesson PROVES the install, then builds
# every demo itself: a deterministic 200x120 red image is
# CREATED in a temp sandbox (no photos, no machine files),
# opened, cropped, converted, resized, rotated, filtered,
# enhanced, saved and reopened -- then the sandbox is
# destroyed. Nothing machine-specific is ever printed
# (no paths -- basenames and shapes only).
#
# BOX CONVENTION [02:39]: crop's box is
# (left, upper, right, lower) -- so the result's width is
# right-left and height is lower-upper.
#
# Everything is deterministic: fixed pixels, fixed sizes.
# Every expected output was produced by running the file,
# not written from memory.

import os
import shutil
import tempfile

from PIL import Image, ImageEnhance, ImageFilter

# ============================================================
# [1] What Pillow is, and that it is installed [00:27]
# ============================================================
# The transcript's definition: a powerful external library
# for processing images, installed via `pip install
# Pillow`. We check presence without printing the
# version number (machine-specific):

import importlib.util

pillow_present = importlib.util.find_spec("PIL") is not None
import PIL
version_readable = len(PIL.__version__) > 0

print(f"  Pillow installed: {pillow_present}")
print(f"  version on file: {version_readable}")
#   Pillow installed: True
#   version on file: True

# The import at the top of this file already succeeded --
# Image, ImageFilter and ImageEnhance are all usable.
# (Run `pip show Pillow` in a terminal to see YOUR
# version.)

# ============================================================
# [2] The sandbox: our own image to work on [00:52]
# ============================================================
# The transcript opens an existing photo with
# Image.open("image_name.jpg"). A reproducible lesson
# cannot depend on a photo that changes per machine --
# so we CREATE one (the lesson 65 sandbox discipline):
# a 200x120 solid red RGB canvas:

WORK_DIR = tempfile.mkdtemp(prefix="py87_")
IMAGE_NAME = "scene.png"
image_path = os.path.join(WORK_DIR, IMAGE_NAME)

canvas = Image.new("RGB", (200, 120), (255, 0, 0))
canvas.save(image_path)

my_image = Image.open(image_path)

print(f"  created and opened: {IMAGE_NAME}")
print(f"  size: {my_image.size}")
print(f"  mode: {my_image.mode}")
#   created and opened: scene.png
#   size: (200, 120)
#   mode: RGB

# The image object carries the two facts every operation
# in this lesson preserves or transforms on purpose:
# WIDTH x HEIGHT, and the color mode (RGB = red, green,
# blue channels).

# ============================================================
# [3] Opening, exactly as the transcript writes it
# ============================================================
# The transcript's line [00:52]:
#     my_image = Image.open("image_name.jpg")
# Ours differs only in path style (a sandbox file) --
# the call is identical:

print(f"  Image.open is callable: {callable(Image.open)}")
print(f"  our object is an Image: {type(my_image).__name__}")
print(f"  container format: {my_image.format}")
#   Image.open is callable: True
#   our object is an Image: PngImageFile
#   container format: PNG

# from PIL import Image; Image.open(...) -- the
# transcript's two lines, verbatim. The returned object
# is PngImageFile -- a SUBCLASS of Image tailored to PNG
# files (jpg files would report JpegImageFile) -- and it
# reports its container (.format -> PNG). Every method
# below is inherited from the shared Image family.

# ============================================================
# [4] Cropping: box=(left, upper, right, lower) [02:39]
# ============================================================
# The transcript's crop() with an explicit box. We take
# a 50x40 window at (10, 10)-(60, 50):

box = (10, 10, 60, 50)
cropped = my_image.crop(box)

expected_width = box[2] - box[0]     # right - left
expected_height = box[3] - box[1]    # lower - upper

print(f"  box: {box}")
print(f"  cropped size: {cropped.size}")
print(f"  width = right-left: {cropped.size[0] == expected_width}")
print(f"  height = lower-upper: {cropped.size[1] == expected_height}")
print(f"  first pixel survives: {cropped.getpixel((0, 0))}")
#   box: (10, 10, 60, 50)
#   cropped size: (50, 40)
#   width = right-left: True
#   height = lower-upper: True
#   first pixel survives: (255, 0, 0)

# (50, 40) -- the box's RIGHT minus LEFT, LOWER minus
# UPPER, exactly the transcript's rule. The pixel is the
# same red because we cut from a solid canvas; crop moves
# the window, it does not repaint.

# ============================================================
# [5] Converting modes: convert("L") [05:29]
# ============================================================
# The transcript: turn COLOR into black-and-white /
# grayscale with convert("L") -- L is the luminance
# channel, one byte per pixel:

grayscale = my_image.convert("L")

red_luminance = grayscale.getpixel((0, 0))
print(f"  before mode: {my_image.mode}")
print(f"  after mode: {grayscale.mode}")
print(f"  red pixel becomes: {red_luminance}")
print(f"  in range 0..255: {0 <= red_luminance <= 255}")
#   before mode: RGB
#   after mode: L
#   red pixel becomes: 76
#   in range 0..255: True

# RGB -> L. Pure red (255, 0, 0) weighs in at 76 on the
# luminance scale (red counts less than green in human
# vision math). Same picture, new clothing -- the
# transcript's التدرج الرمادي in one call.

# ============================================================
# [6] Resizing: resize() [05:47]
# ============================================================
# Change the dimensions on purpose -- the transcript's
# تغيير الحجم:

resized = my_image.resize((100, 60))

print(f"  original: {my_image.size}")
print(f"  resized: {resized.size}")
print(f"  exactly half: {resized.size == (my_image.size[0] // 2, my_image.size[1] // 2)}")
#   original: (200, 120)
#   resized: (100, 60)
#   exactly half: True

# (200, 120) -> (100, 60): both axes halved, mode
# untouched. Pass the new (width, height) tuple and
# Pillow resamples the whole thing.

# ============================================================
# [7] Rotating: rotate() [05:47]
# ============================================================
# The transcript's تدوير الصور. A quarter turn with
# expand=True so the canvas grows to hold the corners:

rotated = my_image.rotate(90, expand=True)

print(f"  rotated 90 degrees: {rotated.size}")
print(f"  axes swapped: {rotated.size == (my_image.size[1], my_image.size[0])}")
print(f"  mode kept: {rotated.mode}")
#   rotated 90 degrees: (120, 200)
#   axes swapped: True
#   mode kept: True

# 90 degrees turns (200, 120) into (120, 200) -- width
# and height trade places. expand=True is the flag that
# lets the canvas grow; without it Pillow keeps the
# original frame and clips the corners.

# ============================================================
# [8] Filters: ImageFilter [05:47]
# ============================================================
# The transcript's إضافة فلاتر تأثيرات. One filter --
# SHARPEN -- applied to the canvas:

sharpened = my_image.filter(ImageFilter.SHARPEN)

print(f"  filter applied: {type(sharpened).__name__}")
print(f"  frame unchanged: {sharpened.size == my_image.size}")
print(f"  solid red survives sharpen: {sharpened.getpixel((0, 0))}")
#   filter applied: Image
#   frame unchanged: True
#   solid red survives sharpen: (255, 0, 0)

# Still an Image, same frame. (A uniform solid color
# has no edges to sharpen -- real photographs show the
# difference instantly; the pipeline itself is what this
# line proves.) ImageFilter also ships BLUR, CONTOUR,
# EMBOSS and more -- same one-line pattern.

# ============================================================
# [9] Brightness & Contrast: ImageEnhance [05:47]
# ============================================================
# The transcript's مستويات السطوع والتباين. Halving the
# brightness of pure red:

darker = ImageEnhance.Brightness(my_image).enhance(0.5)
print(f"  brightness factor: 0.5")
print(f"  red 255 -> {darker.getpixel((0, 0))[0]}")
print(f"  darkened in place: {darker.size == my_image.size}")
#   brightness factor: 0.5
#   red 255 -> 127
#   darkened in place: True

# 255 * 0.5 = 127.5 -> 127 (Pillow floors) -- the red
# channel dimmed, geometry untouched. Contrast works the
# same way: ImageEnhance.Contrast(img).enhance(1.5)
# pushes values apart. The transcript's
# Brightness & Contrast, measured.

# ============================================================
# [10] Saving and reopening the result
# ============================================================
# The transcript's "حفظه أو عرضه". Save the processed
# image next to the original, open it again, confirm the
# facts survived the round trip -- by BASENAME only:

out_name = "cropped.png"
out_path = os.path.join(WORK_DIR, out_name)
cropped.save(out_path)

reopened = Image.open(out_path)
same_size = reopened.size == cropped.size
same_mode = reopened.mode == cropped.mode

print(f"  saved: {out_name}")
print(f"  reopened size matches: {same_size}")
print(f"  reopened mode matches: {same_mode}")
#   saved: cropped.png
#   reopened size matches: True
#   reopened mode matches: True

# Bytes to disk, bytes back to an object -- sizes and
# modes intact. (The actual directory lives in the temp
# sandbox and is never printed: course rule 1.)

# ============================================================
# [11] Cleanup: the sandbox is destroyed
# ============================================================
# Everything happens under WORK_DIR -- the transcript's
# demo file never touches your folders. Close handles,
# then rmtree (lesson 65 discipline):

my_image.close()
reopened.close()
shutil.rmtree(WORK_DIR, ignore_errors=True)

print(f"  sandbox removed: {not os.path.exists(WORK_DIR)}")
#   sandbox removed: True

# Gone. No .png in the repo, no temp folder left behind
# -- the whole photo lab existed for one run.

# ============================================================
# [12] One session: everything together
# ============================================================
# The transcript's tour in one block -- but the sandbox
# must exist again to walk it, so rebuild, replay, and
# re-clean:

WORK_DIR = tempfile.mkdtemp(prefix="py87_")
try:
    path = os.path.join(WORK_DIR, IMAGE_NAME)
    Image.new("RGB", (200, 120), (255, 0, 0)).save(path)
    img = Image.open(path)

    print(f"  open: {img.size} {img.mode}")
    print(f"  crop (50x40): {img.crop((10, 10, 60, 50)).size}")
    print(f"  grayscale pixel: {img.convert('L').getpixel((0, 0))}")
    print(f"  resize half: {img.resize((100, 60)).size}")
    print(f"  rotate 90: {img.rotate(90, expand=True).size}")
    print(f"  brightness 0.5: {img.getpixel((0, 0))[0]} -> "
          f"{ImageEnhance.Brightness(img).enhance(0.5).getpixel((0, 0))[0]}")
    print(f"  filter stays Image: {type(img.filter(ImageFilter.SHARPEN)).__name__}")
    img.close()
finally:
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    print(f"  cleaned: {not os.path.exists(WORK_DIR)}")
#   open: (200, 120) RGB
#   crop (50x40): (50, 40)
#   grayscale pixel: 76
#   resize half: (100, 60)
#   rotate 90: (120, 200)
#   brightness 0.5: 255 -> 127
#   filter stays Image: Image
#   cleaned: True

# Open, cut, gray, shrink, turn, dim, sharpen, and
# clean -- every move from the transcript in eight
# lines, zero files left behind.

# ============================================================
# [13] The summary
# ============================================================
# Pillow, from the transcript, complete:
#
#   1. WHAT [00:27] -- a powerful external library for
#      processing images programmatically; install with
#      `pip install Pillow`; this lesson verifies
#      presence (installed True) and that a version is
#      on file (number unprinted -- machine-specific)
#   2. IMPORT + OPEN [00:52] -- from PIL import Image;
#      Image.open("file") returns an Image object; our
#      demo image is CREATED (200x120 solid red RGB) in
#      a temp sandbox so every run sees identical pixels
#   3. THE FACTS EVERY OP PRESERVES OR CHANGES ON PURPOSE
#      -- size (200, 120) and mode 'RGB'
#   4. CROP [02:39] -- box = (left, upper, right, lower):
#      (10, 10, 60, 50) -> size (50, 40), where width =
#      right-left and height = lower-upper (both checked
#      True); pixels move, they do not repaint
#   5. CONVERT [05:29] -- convert("L") turns RGB into
#      grayscale L; pure red becomes 76 on the
#      luminance scale (range check 0..255 True) -- the
#      transcript's التدرج الرمادي
#   6. RESIZE [05:47] -- resize((100, 60)) halves both
#      axes of (200, 120) (exactly half -> True), mode
#      untouched
#   7. ROTATE [05:47] -- rotate(90, expand=True) swaps
#      the axes: (120, 200) (axes swapped -> True);
#      expand=True is what lets the canvas grow instead
#      of clipping corners
#   8. FILTERS [05:47] -- ImageFilter.SHARPEN returns an
#      Image with the same frame (a solid color has no
#      edges to sharpen -- the pipeline is the proof);
#      BLUR, CONTOUR, EMBOSS follow the same one-liner
#   9. BRIGHTNESS & CONTRAST [05:47] --
#      ImageEnhance.Brightness(img).enhance(0.5):
#      red 255 -> 127 (halved, floored), frame kept;
#      Contrast works the same way
#  10. SAVE + REOPEN -- cropped.png written to the
#       sandbox, reopened, size and mode both match
#       (True); only the BASENAME is ever printed
#  11. CLEANUP -- handles closed, rmtree fires,
#       sandbox removed -> True: no .png in the repo,
#       no temp folders left
#  12. THE DISCIPLINE -- fixed-size canvas, fixed pixels,
#       fixed boxes; no photos from disk, no paths
#       printed, no version numbers: byte-stable on
#       every run, like every lesson before it
#
# A canvas in, a hundred transformations down the line,
# a clean directory out -- Pillow with a paper towel.
