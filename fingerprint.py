import fingerpi as fp
def printByteArray(arr):
    return map(hex, list(arr))
f = fp.FingerPi()
f.Open(extra_info = True, check_baudrate = True)
f.ChangeBaudrate(115200)
f.CmosLed(True)
f.CaptureFinger()
f.CmosLed(False)
response = f.GetImage()
print response
f.Close()

#CheckEnrolled
#EnrollStart
#Enroll1
#Enroll2
#Enroll3
#IsPressFinger
#DeleteId
#DeleteAll
#Identify
#VerifyTemplate
#IdentifyTemplate
#CaptureFinger
#MakeTemplate
#GetImage
#GetRawImage
#GetTemplate
