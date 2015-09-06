from __future__ import division
from collections import Counter

from django.shortcuts import render

import matplotlib
matplotlib.use('Agg')

from matplotlib import pylab
from pylab import *

import PIL
import PIL.Image
import StringIO

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
#from django.template.context_processors import csrf
from django.core.context_processors import csrf

def index(request):
    if request.POST.get('segregationCoefficient') != None:
        has_image = True
        sc = request.POST.get('segregationCoefficient')
        c = request.POST.get('concentration')
        wa = request.POST.get('wellAlloy')
        wl = request.POST.get('wellLength')
        rba = request.POST.get('rightBarrierAlloy')
        rbl = request.POST.get('rightBarrierLength')
        
        context = { 'has_image': has_image, 'sc': sc, 'c': c, 'wa': wa, 'wl': wl, 'rba': rba, 'rbl': rbl }
    else:
        has_image = False
        context = { 'has_image': has_image }
    
    context.update(csrf(request))
    return render_to_response("muraki/index.html", context)
    #return HttpResponse("Hello <img src='/sample_graph/'>")
    
def muraki_graph(request):
    
    # Get current size
    fig_size = rcParams["figure.figsize"]
    # Set figure width to 12 and height to 9
    fig_size[0] = 8
    fig_size[1] = 6
    rcParams["figure.figsize"] = fig_size
    
    db = [6.0584, 5.65325]
    segregationCoefficient = float(request.GET.get('sc'))
    concentration = float(request.GET.get('c'))
    aWellAlloy = db[int(request.GET.get('wa'))]
    wellLength = float(request.GET.get('wl'))
    aRightBarrierAlloy = db[int(request.GET.get('rba'))]
    rightBarrierLength = float(request.GET.get('rbl'))
    place = request.GET.get('p') # i or o, for inside or outside
    temp = int(request.GET.get('temp')) # 0 for contentration
    
    latticeParam = aWellAlloy * concentration + aRightBarrierAlloy * (1 - concentration)
    
    wellMonoLayers = int((2 * wellLength) // latticeParam)
    rightBarrierMonoLayers = int((2 * rightBarrierLength) // aRightBarrierAlloy)
    
    concentrationInsideWell = lambda n: concentration * (1 - segregationCoefficient ** n)
    concentrationOutsideWell = lambda n: concentration * (1 - segregationCoefficient ** n) * (segregationCoefficient ** (n - wellMonoLayers))
    
    e2InGaAs = lambda n: 1.5192 - 1.5837 * n + 0.475 * (n ** 2)
    e77InGaAs = lambda n: 1.508 - 1.47 * n + 0.375 * (n ** 2)
    e300InGaAs = lambda n: 1.43 - 1.53 * n + 0.45 * (n ** 2)
    
    
    gTitle = ''
    yTitle = ''
    if place == 'i':
        layers = [l for l in xrange(1, wellMonoLayers + 1)]
        wellPoints = [concentrationInsideWell(n) for n in xrange(1, wellMonoLayers + 1)]
        yTitle = "Energy (eV)"
        if temp == 2:
            wellPoints = [e2InGaAs(x) for x in wellPoints]
            gTitle = "Well layers energy at 2 K"
        elif temp == 77:
            wellPoints = [e77InGaAs(x) for x in wellPoints]
            gTitle = "Well layers energy at 77 K"
        elif temp == 300:
            wellPoints = [e300InGaAs(x) for x in wellPoints]
            gTitle = "Well layers energy at 300 K"
        else:
            gTitle = "In Concentration Inside Well"
            yTitle = "In Concentration (%)"
    else:
        layers = [l for l in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
        wellPoints = [concentrationOutsideWell(n) for n in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
        gTitle = "In Concentration Outside Well"
        yTitle = "In Concentration (%)"
    
    step(layers, wellPoints, color='green', marker='', linestyle='solid')
    title(gTitle)
    xlabel("Layer")
    ylabel(yTitle)
    
    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    return HttpResponse(buffer.getvalue(), content_type="image/png")
    
def in_concentration_graph(request):
    db = [6.0584, 5.65325]
    segregationCoefficient = float(request.GET.get('sc'))
    concentration = float(request.GET.get('c'))
    aWellAlloy = db[int(request.GET.get('wa'))]
    wellLength = float(request.GET.get('wl'))
    aRightBarrierAlloy = db[int(request.GET.get('rba'))]
    rightBarrierLength = float(request.GET.get('rbl'))
    
    latticeParam = aWellAlloy * concentration + aRightBarrierAlloy * (1 - concentration)
    
    wellMonoLayers = int((2 * wellLength) // latticeParam)
    rightBarrierMonoLayers = int((2 * rightBarrierLength) // aRightBarrierAlloy)
    
    concentrationInsideWell = lambda n: concentration * (1 - segregationCoefficient ** n)
    concentrationOutsideWell = lambda n: concentration * (1 - segregationCoefficient ** n) * (segregationCoefficient ** (n - wellMonoLayers))
    
    gTitle = ''
    yTitle = 'In Concentration (%)'
    
    
    # Get current size
    fig_size = rcParams["figure.figsize"]
    # Set figure width to 12 and height to 9
    fig_size[0] = 12
    fig_size[1] = 6
    rcParams["figure.figsize"] = fig_size
    
    f, (ax1, ax2) = subplots(1, 2, sharey=True)
    
    layers = [l for l in xrange(1, wellMonoLayers + 1)]
    wellPoints = [concentrationInsideWell(n) for n in xrange(1, wellMonoLayers + 1)]
    yTitle = "Energy (eV)"
    gTitle = "In Concentration Inside Well"
    
    ax1.step(layers, wellPoints, color='green', marker='', linestyle='solid')
    ax1.set_title(gTitle)
    ax1.set_xlabel("Layer")
    ax1.set_ylabel(yTitle)
    
    layers = [l for l in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
    wellPoints = [concentrationOutsideWell(n) for n in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
    gTitle = "In Concentration Outside Well"
    
    ax2.step(layers, wellPoints, color='green', marker='', linestyle='solid')
    ax2.set_title(gTitle)
    ax2.set_xlabel("Layer")
    ax2.set_ylabel(yTitle)
        
    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    return HttpResponse(buffer.getvalue(), content_type="image/png")
    
def in_energies_graph(request):
    db = [6.0584, 5.65325]
    segregationCoefficient = float(request.GET.get('sc'))
    concentration = float(request.GET.get('c'))
    aWellAlloy = db[int(request.GET.get('wa'))]
    wellLength = float(request.GET.get('wl'))
    aRightBarrierAlloy = db[int(request.GET.get('rba'))]
    rightBarrierLength = float(request.GET.get('rbl'))
    latticeParam = aWellAlloy * concentration + aRightBarrierAlloy * (1 - concentration)
    wellMonoLayers = int((2 * wellLength) // latticeParam)
    rightBarrierMonoLayers = int((2 * rightBarrierLength) // aRightBarrierAlloy)
    
    concentrationInsideWell = lambda n: concentration * (1 - segregationCoefficient ** n)
    concentrationOutsideWell = lambda n: concentration * (1 - segregationCoefficient ** n) * (segregationCoefficient ** (n - wellMonoLayers))
    
    gTitle = ''
    yTitle = 'In Concentration (%)'
    
    # Get current size
    fig_size = rcParams["figure.figsize"]
    # Set figure width to 12 and height to 9
    fig_size[0] = 12
    fig_size[1] = 6
    rcParams["figure.figsize"] = fig_size
    
    f, (ax1, ax2) = subplots(1, 2, sharey=True)
    
    layers = [l for l in xrange(1, wellMonoLayers + 1)]
    wellPoints = [concentrationInsideWell(n) for n in xrange(1, wellMonoLayers + 1)]
    yTitle = "Energy (eV)"
    gTitle = "In Concentration Inside Well"
    
    ax1.step(layers, wellPoints, color='green', marker='', linestyle='solid')
    ax1.set_title(gTitle)
    ax1.set_xlabel("Layer")
    ax1.set_ylabel(yTitle)
    
    layers = [l for l in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
    wellPoints = [concentrationOutsideWell(n) for n in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
    gTitle = "In Concentration Outside Well"
    
    ax2.step(layers, wellPoints, color='green', marker='', linestyle='solid')
    ax2.set_title(gTitle)
    ax2.set_xlabel("Layer")
    ax2.set_ylabel(yTitle)
        
    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    return HttpResponse(buffer.getvalue(), content_type="image/png")

def strained_well(request):
    # GaAs parameters
    aGaAs = 5.65325
    acGaAs = -7.17
    avGaAs = 1.16
    bGaAs = -1.70
    c11GaAs = 11.879
    c12GaAs = 5.376
    meGaAs = 0.067
    deltaGaAs = 0.34
    
    # InAs parameters
    aInAs = 6.0584
    acInAs = -5.08
    avInAs = 1.00
    bInAs = -1.80
    c11InAs = 8.329
    c12InAs = 4.526
    meInAs = 0.023
    deltaInAs = 0.38
    
    # InGaAs gap
    eg2 = lambda x: 1.5192 - 1.5837 * x + 0.475 * x ** 2
    eg77 = lambda x: 1.508 - 1.47 * x + 0.375 * x ** 2
    eg300 = lambda x: 1.43 - 1.53 * x + 0.45 * x ** 2
    
    
    
    db = [6.0584, 5.65325]
    
    segregationCoefficient = float(request.GET.get('sc'))
    concentration = float(request.GET.get('c'))
    aWellAlloy = db[int(request.GET.get('wa'))]
    wellLength = float(request.GET.get('wl'))
    aRightBarrierAlloy = db[int(request.GET.get('rba'))]
    rightBarrierLength = float(request.GET.get('rbl'))
    
    latticeParam = aWellAlloy * concentration + aRightBarrierAlloy * (1 - concentration)
    wellMonoLayers = int((2 * wellLength) // latticeParam)
    rightBarrierMonoLayers = int((2 * rightBarrierLength) // aRightBarrierAlloy)
    
    concentrationInsideWell = lambda n: concentration * (1 - segregationCoefficient ** n)
    concentrationOutsideWell = lambda n: concentration * (1 - segregationCoefficient ** n) * (segregationCoefficient ** (n - wellMonoLayers))
    
    gTitle = ''
    yTitle = 'In Concentration (%)'
    
    # Get current size
    fig_size = rcParams["figure.figsize"]
    # Set figure width to 12 and height to 9
    fig_size[0] = 12
    fig_size[1] = 6
    rcParams["figure.figsize"] = fig_size
    
    f, (ax1, ax2) = subplots(1, 2, sharey=True)
    
    layers = [l for l in xrange(1, wellMonoLayers + 1)]
    wellPoints = [concentrationInsideWell(n) for n in xrange(1, wellMonoLayers + 1)]
    yTitle = "Energy (eV)"
    gTitle = "In Concentration Inside Well"
    
    ax1.step(layers, wellPoints, color='green', marker='', linestyle='solid')
    ax1.set_title(gTitle)
    ax1.set_xlabel("Layer")
    ax1.set_ylabel(yTitle)
    
    layers = [l for l in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
    wellPoints = [concentrationOutsideWell(n) for n in xrange(wellMonoLayers + 1, rightBarrierMonoLayers + 1)]
    gTitle = "In Concentration Outside Well"
    
    ax2.step(layers, wellPoints, color='green', marker='', linestyle='solid')
    ax2.set_title(gTitle)
    ax2.set_xlabel("Layer")
    ax2.set_ylabel(yTitle)
        
    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    return HttpResponse(buffer.getvalue(), content_type="image/png")
    
