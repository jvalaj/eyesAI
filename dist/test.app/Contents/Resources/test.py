import sys
from Cocoa import NSApplication, NSWindow, NSRect, NSBackingStoreBuffered, NSColor, NSView
from AppKit import NSScreen, NSStatusWindowLevel
from PyObjCTools import AppHelper

class OverlayView(NSView):
    def drawRect_(self, rect):
        NSColor.clearColor().setFill()
        self.bounds().fill()
        NSColor.redColor().setStroke()
        rect = NSRect((940, 430), (1110-940, 680-430))
        path = NSBezierPath.bezierPathWithRect_(rect)
        path.setLineWidth_(4.0)
        path.stroke()

class OverlayWindow(NSWindow):
    def canBecomeKeyWindow(self):
        return True

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    screen = NSScreen.mainScreen().frame()
    window = OverlayWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        screen,
        0x1 | 0x1000,  # borderless + non-activating panel
        NSBackingStoreBuffered,
        False
    )
    window.setLevel_(NSStatusWindowLevel + 1)
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.setIgnoresMouseEvents_(True)
    window.setAlphaValue_(0.5)
    window.setContentView_(OverlayView.alloc().initWithFrame_(screen))
    window.orderFrontRegardless()
    app.activateIgnoringOtherApps_(True)
    AppHelper.runEventLoop()
