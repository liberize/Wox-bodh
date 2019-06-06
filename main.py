# -*- coding: utf-8 -*-

from wox import Wox
import subprocess
import re


def toDec(dec, padding):
    return ("{dec:0{padding}d}".format(dec=dec, padding=padding), "Dec")


def toHex(dec, padding):
    return ("0x{dec:0{padding}x}".format(dec=dec, padding=padding), "Hex")


def toOct(dec, padding):
    return ("0{dec:0{padding}o}".format(dec=dec, padding=padding), "Oct")


def toBin(dec, padding):
    return ("b{dec:0{padding}b}".format(dec=dec, padding=padding), "Bin")


def getDec(arg):
    if arg.startswith("0x") or arg.startswith("0X"):
        return (int(arg, 0), "Hex")
    elif isBin(arg):
        return (int(arg, 2), "Bin")
    elif arg.startswith("0"):
        return (int(arg, 8), "Oct")
    else:
        return (int(arg, 10), "Dec")


def isBin(arg):
    result = re.match("[10]+", arg)
    return result is not None and len(result.group()) == len(arg)


class Bodh(Wox):
    converters = [toDec, toHex, toBin, toOct]

    def query(self, query):
        results = []
        if len(query) == 0:
            return results
        try:
            decResult = getDec(query)
            for func in self.converters:
                result = func(decResult[0], 1)
                if result[1] != decResult[1]:
                    results.append({
                        "Title": result[0],
                        "SubTitle": "To {t}, copy to clipboard".format(t=result[1]),
                        "IcoPath": "Images/app.png",
                        'JsonRPCAction': {
                            'method': 'copyToClipboard',
                            'parameters': [result[0]],
                            'dontHideAfterAction': False
                        }
                    })
                pass
        except Exception as e:
            results = []
            results.append({
                "Title": "Invalid parameters",
                "SubTitle": "Please try again",
                "IcoPath": 'Images/app.png'
            })
            return results
        return results

    def copyToClipboard(self, value):
        p = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE)
        p.stdin.write(value.encode('gbk'))
        p.stdin.close()


if __name__ == "__main__":
    Bodh()
