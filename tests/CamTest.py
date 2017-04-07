from Coliform import RPiCameraBackend

camera = RPiCameraBackend.PiCamera()
camera.resolution = (2952, 1944)
camera.brightness = 50
camera.contrast = 0
camera.iso = 0
camera.zoom = (0.0, 0.0, 1.0, 1.0)
camera.timeout = 20000
camera.timelapse = 5000
camera.quality = 75
camera.exposure_mode = ''
camera.awb_mode = ''
camera.preview = (100, 100, 300, 200)
camera.capture(mode='JPG', filename='image%04d.jpg')