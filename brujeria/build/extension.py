# Please note, templates are handled according to the following.

# Within an extension root file, a series of custom pragmas are added to the
# source. These are "special" pragmas in that we pull them out and extract them
# but don't act like a full C preprocessor. One can put an #if 0 around them
# and we would still extract them. What we may want to do is parse comments
# and support that within our own stuff, but that can come later...
# An example of this syntax is as follows:

# #pragma brujeria compiler("flags", "-std=c++17", "-funroll-loops")
# #pragma brujeria linker("/LTCG", "Dad", "why?")
# #pragma brujeria library("package-name", "library-name")
# #pragma brujeria library("library-name")
# #pragma brujeria library("winsock2", platform="windows")
# #pragma brujeria sources("Additional/Sources/")

# More pragmas will be added over time to support additional paths, and *some*
# python logic (platform specific stuff, as well as find_library, cmake/meson
# support, etc.)

# These notes are being placed here for safe keeping.