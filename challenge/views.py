from collections import OrderedDict

from datadog import statsd
from django.http import Http404
from django.shortcuts import render

from challenge.urlnames import ChallengeUrlNames

RANDOM_DATA = [
    804864, 285355, 280581, 257234, 999434, 456715, 964620, 124941, 659473, 636946, 921528, 781386, 710677, 210966,
    725017, 942113, 745311, 444452, 812893, 112679, 751858, 509994, 610348, 117705, 149551, 403504, 960520, 895027,
    135220, 487477, 999478, 825399, 570049, 182282, 237630, 524352, 460865, 215106, 530499, 120901, 305222, 983113,
    997047, 598094, 960525, 491601, 322915, 366679, 391259, 770140, 351074, 522343, 768104, 891384, 514159, 155761,
    340082, 385139, 876660, 106615, 366714, 564927, 972925, 755838, 841749, 137346, 422019, 852100, 350341, 116871,
    970888, 758807, 616589, 636269, 211089, 524436, 215190, 395415, 362240, 182426, 111983, 778398, 118944, 630949,
    213165, 301230, 481455, 759705, 569521, 927922, 864435, 174260, 854199, 223416, 641209, 209503, 889022, 916853,
    325824, 274626, 511691, 891076, 766151, 356553, 183671, 757964, 317647, 545740, 800978, 364755, 788694, 677241,
    860376, 889050, 155867, 979165, 561374, 319711, 102625, 516324, 821477, 348392, 844009, 674026, 909548, 207085,
    934127, 651504, 248050, 665844, 491766, 389369, 732145, 659708, 767361, 903893, 467207, 889900, 240035, 268674,
    514093, 741650, 932115, 223510, 416025, 385306, 791258, 375070, 323874, 200995, 629030, 807985, 928041, 901418,
    186667, 917804, 144039, 158974, 379614, 467255, 901432, 321849, 809697, 977217, 510864, 284995, 340294, 170311,
    133453, 344398, 893667, 633177, 813673, 914491, 937702, 979305, 618862, 480317, 915824, 878440, 317810, 802195,
    751678, 323962, 256380, 754050, 992794, 307588, 364934, 942145, 401800, 887532, 121227, 174477, 967057, 684434,
    102467, 375190, 536985, 831897, 590234, 192928, 747506, 938403, 563621, 432551, 616872, 301482, 278957, 199086,
    876975, 663985, 209330, 375219, 582068, 306963, 924089, 567741, 168383, 969154, 807363, 836039, 803272, 606665,
    113099, 629197, 874958, 575952, 279288, 446930, 123347, 515995, 312398, 809430, 700889, 512475, 960991, 680417,
    291298, 502249, 711147, 141805, 444913, 950771, 864759, 934392, 922499, 860670, 653823, 295425, 199170, 754181,
    152079, 551440, 952849, 369171, 279060, 241070, 592411, 530973, 414239, 686626, 578083, 539172, 265649, 266792,
    453163, 266796, 821806, 725551, 286131, 817720, 279097, 469562, 111164, 657981, 589788, 578112, 864833, 315970,
    408131, 852549, 667089, 668231, 244296, 143948, 870864, 592463, 899665, 899666, 141910, 714169, 903768, 258649,
    551515, 707165, 387678, 111199, 449120, 209506, 342627, 784997, 709279, 948841, 965226, 184940, 365167, 293488,
    300286, 567923, 760436, 645749, 533112, 320385, 688763, 170621, 909953, 348803, 633480, 438042, 624749, 504259,
    950932, 156309, 109206, 453271, 636698, 950942, 641695, 604835, 743537, 647851, 936621, 600753, 983731, 379573,
    486071, 725688, 789179, 970186, 334528, 758465, 871107, 469702, 822190, 801480, 412362, 256715, 645836, 759017,
    434894, 448973, 324294, 107221, 471766, 936663, 101156, 643802, 738016, 258782, 948960, 107233, 505354, 131811,
    576228, 959205, 924390, 779637, 834280, 520937, 682732, 480722, 307950, 910063, 525041, 461554, 807667, 174836,
    432254, 326392, 563962, 504571, 490236, 998142, 754475, 750038, 707334, 670474, 876135, 994434, 289552, 908050,
    336003, 289556, 113432, 561947, 496416, 162593, 314843, 783140, 123687, 957227, 615212, 865069, 541486, 697137,
    834356, 772924, 932677, 881479, 543884, 787210, 406348, 336719, 785235, 344916, 691532, 787290, 179036, 183134,
    750432, 131937, 516962, 187235, 404594, 564071, 737701, 161597, 727920, 445298, 514932, 283515, 482176, 514945,
    490370, 963051, 951172, 211850, 750475, 889744, 523159, 955289, 336794, 637852, 731973, 106786, 613283, 750065,
    478121, 699307, 680876, 578477, 539566, 801712, 720791, 598965, 594870, 945079, 599062, 953277, 865216, 791712,
    707524, 171203, 753484, 429002, 320459, 783308, 330701, 609230, 967633, 625618, 676819, 531412, 510934, 709591,
    271183, 537564, 488414, 451551, 510944, 515041, 141075, 961507, 314343, 541674, 946924, 139090, 285680, 715761,
    949234, 404467, 490484, 873462, 209911, 670715, 121853, 775169, 947204, 805894, 158209, 599049, 988935, 943121,
    676882, 115731, 275477, 545814, 310295, 379928, 873499, 320540, 588154, 193569, 357410, 668707, 707621, 867366,
    629596, 289834, 304172, 648237, 994351, 969777, 234546, 492595, 318516, 621622, 226361, 275515, 898108, 654397,
    859200, 511043, 375876, 545862, 982087, 975944, 554058, 226487, 107362, 803918, 228431, 996195, 957527, 590936,
    216154, 302171, 343132, 275551, 756832, 661008, 416866, 263273, 205934, 664687, 855912, 594499, 168126, 400233,
    674324, 197756, 196578, 777346, 597123, 126828, 373899, 991944, 415938, 572558, 597135, 382096, 873618, 509075,
    322877, 404631, 104303, 674972, 421402, 398494, 248992, 666785, 107682, 101540, 246951, 891421, 552115, 658612,
    302622, 643273, 509115, 197821, 707778, 389323, 643398, 158917, 130251, 791757, 826574, 400594, 238804, 972665,
    742616, 566491, 279773, 605409, 725565, 824550, 745340, 320746, 277739, 750828, 478445, 122094, 207400, 326903,
    732411, 496894, 503039, 396545, 720131, 681220, 402693, 134407, 709164, 832778, 695563, 701708, 635778, 228626,
    750867, 529684, 480277, 260314, 517406, 767268, 496934, 898609, 431401, 378155, 781613, 515375, 847152, 671283,
    774025, 958004, 308538, 847164, 607114, 408896, 961857, 716100, 955722, 265547, 834892, 703821, 326990, 996687,
    959825, 486742, 572985, 631537, 404830, 443743, 521104, 245307, 353637, 494952, 640365, 988527, 298356, 302654,
    949622, 750967, 156419, 257401, 445819, 527741, 275838, 546175, 232832, 265601, 501123, 636297, 510871, 857484,
    798093, 622829, 126353, 136595, 124310, 869783, 880026, 144795, 310685, 163230, 890271, 474528, 253346, 972699,
    757158, 365996, 466349, 749450, 834120, 873907, 126390, 480697, 574908, 277950, 593345, 994754, 810571, 235624,
    435653, 724426, 904651, 363980, 495057, 122322, 634323, 531925, 124374, 437719, 218584, 404953, 194127, 675292,
    794078, 764182, 781796, 706021, 945640, 514859, 574957, 681454, 302578, 306676, 654837, 845302, 986616, 894460,
    456191, 998915, 376324, 749061, 648712, 685996, 809738, 312844, 591375, 935440, 866904, 183826, 873731, 173589,
    103959, 630297, 284186, 744989, 232990, 927664, 874466, 820771, 493093, 411175, 558634, 459015, 464818, 565853,
    200241, 100275, 282164, 321077, 663096, 861753, 788027, 342736, 339518, 765503, 996928, 941633, 574731, 650822,
    382699, 955976, 501323, 419404, 491087, 775761, 128594, 443988, 573014, 773723, 847452, 109498, 310879, 257634,
    489061, 974439, 906856, 900713, 542314, 980587, 464492, 562797, 438205, 628340, 790135, 660756, 237179, 910972,
    636541, 419456, 415362, 763523, 811286, 824967, 226954, 151179, 833172, 841368, 691866, 579719, 339614, 214691,
    237220, 628393, 200362, 493228, 218798, 243377, 685746, 958132, 163857, 861129, 970425, 145084, 991178, 827071,
    461810, 444098, 210628, 149189, 980438, 685004, 700107, 673967, 841422, 713677, 943825, 132818, 780216, 794325,
    102102, 237271, 800472, 259679, 542435, 607973, 206566, 988903, 919272, 792299, 411372, 904941, 763825, 929362,
    853746, 117715, 823593, 971732, 304893, 536320, 270081, 696071, 257802, 234455, 478992, 565011, 333588, 522006,
    712471, 386840, 446234, 634654, 253728, 736560, 253730, 565029, 901425, 714537, 622379, 612145, 421682, 923771,
    323382, 347960, 239420, 743229, 573247, 474944, 759161, 536388, 255814, 259635, 370504, 651084, 898893, 544590,
    542545, 110418, 194873, 177303, 491357, 589662, 161765, 452451, 259942, 360295, 649064, 421740, 986429, 159641,
    900979, 202613, 673654, 413559, 894840, 149369, 366460, 221154, 186244, 876421, 857991, 501641, 540705, 567179,
    696204, 556945, 577427, 823278, 685567, 752964, 130971, 937886, 372643, 438180, 411557, 426993, 176041, 450474,
    870316, 774130, 417711, 647088, 325553, 106943, 180147, 499638, 548791, 126904, 869364, 477855, 645053, 512556,
    767938, 949579, 270276, 942070, 582866, 577481, 513994, 771405, 496599, 559097, 409252, 325595, 997927, 145801,
    542315, 501730, 188389, 716775, 269099, 991210, 282603, 153580, 989166, 119805, 712689, 726351, 147795, 714740,
    571382, 663544, 227321, 217082, 942075, 804891
]

LINKS = OrderedDict()
for i, id in enumerate(RANDOM_DATA):
    LINKS.update({id: i})
LINK_LIST = LINKS.items()

@statsd.timed('challenge.get.index')
def index_get(request, id=None):
    statsd.increment('challenge.hits.get.index')
    if id is None:
        # start of challenge, render with first id
        return render(request, ChallengeUrlNames.INDEX.template, {'id': LINK_LIST[0][0]})

    id = int(id)
    if id not in LINKS:
        raise Http404()

    next_id_index = LINKS[id] + 1
    if next_id_index == len(RANDOM_DATA):
        return render(request, ChallengeUrlNames.INDEX.template, {'success': True})

    return render(request, ChallengeUrlNames.INDEX.template, {'id': LINK_LIST[next_id_index][0]})