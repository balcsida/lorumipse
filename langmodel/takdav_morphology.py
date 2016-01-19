# coding: utf-8

from scratch import GFactory
import re

def affix(stem, ana):
    if ana.startswith('NOUN'):
        w = GFactory.parseNP(stem)
        if 'NOUN<PLUR>' in ana: w = w.makePlural()
        if '<CAS<ACC>>' in ana: w = w.makeAccusativus()
        if '<CAS<DAT>>' in ana: w = w.makeDativus()
        if '<CAS<DEL>>' in ana: w = w.makeDelativus()
        if '<CAS<ELA>>' in ana: w = w.makeElativus()
        if '<CAS<ABL>>' in ana: w = w.makeAblativus()
        if '<CAS<SUE>>' in ana: w = w.makeSuperessivus()
        if '<CAS<INE>>' in ana: w = w.makeInessivus()
        if '<CAS<ADE>>' in ana: w = w.makeAdessivus()
        if '<CAS<SBL>>' in ana: w = w.makeSublativus()
        if '<CAS<ILL>>' in ana: w = w.makeIllativus()
        if '<CAS<ALL>>' in ana: w = w.makeAllativus()
        if '<CAS<TER>>' in ana: w = w.makeTerminativus()
        if '<CAS<INS>>' in ana: w = w.makeInstrumentalis()
        if '<CAS<CAU>>' in ana: w = w.makeCausalisFinalis()
        if '<CAS<FOR>>' in ana: w = w.makeFormativus()
        if '<CAS<TRA>>' in ana: w = w.makeTranslativusFactivus()
        if '<CAS<TEM>>' in ana: w = w.makeTemporalis()
        return w.ortho
    elif ana.startswith('VERB'):
        w = GFactory.parseV(stem)
        numero = 1
        if '<PLUR>' in ana:
            numero = 3
        person = 3
        if '<PERS<1>>' in ana:
            person = 1
        elif '<PERS<1<OBJ2>>>' in ana:
            person = 1
            definite = 2
        elif '<PERS<2>>' in ana:
            person = 2
        definite = 0
        if '<DEF>' in ana:
            definite = 3
        mood = 1
        if '<COND>' in ana:
            mood = 2
        elif '<SUBJUNC-IMP>' in ana:
            mood = 3
        # todo <MODAL>
        if '<INF>' in ana:
            return w.makeInfinitive(numero, person).ortho
        else:
            return w.conjugate(numero, person, mood, 0, definite).ortho
    return stem


import unittest


class TestMorphology(unittest.TestCase):

    def test_affix(self):
        self.assertEqual(u'tapáljátok', affix(u'tapál', 'VERB<PERS<2>><PLUR><DEF>'))
        self.assertEqual(u'tapáltok', affix(u'tapál', 'VERB<PERS<2>><PLUR>'))

        self.assertEqual(u'futuroknak', affix(u'futur', 'NOUN<PLUR><CAS<DAT>>'))
        self.assertEqual(u'futurt', affix(u'futur', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'vizecskét', affix(u'vizecske', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'anatot', affix(u'anat', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'idülelcsit', affix(u'idülelcsi', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'számeiséget', affix(u'számeiség', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'hátlatikukanipolyát', affix(u'hátlatikukanipolya', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'bangót', affix(u'bangó', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'reklojátumust', affix(u'reklojátumus', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'érmelletet', affix(u'érmellet', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'kasztát', affix(u'kaszta', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'ejtőt', affix(u'ejtő', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'ijedeliletinimberherűségeszténét', affix(u'ijedeliletinimberherűségeszténe', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'tát', affix(u'ta', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'likforanosztást', affix(u'likforanosztás', 'NOUN<CAS<ACC>>'))
        self.assertEqual(u'karhalicskát', affix(u'karhalicska', 'NOUN<CAS<ACC>>'))

        self.assertEqual(u'fiú', affix(u'fiú', 'NOUN')) # nominativus
        self.assertEqual(u'fiút', affix(u'fiú', 'NOUN<CAS<ACC>>')) # accusativus
        self.assertEqual(u'fiúnak', affix(u'fiú', 'NOUN<CAS<DAT>>')) # dativus
        self.assertEqual(u'fiúról', affix(u'fiú', 'NOUN<CAS<DEL>>')) # delativus
        self.assertEqual(u'fiúból', affix(u'fiú', 'NOUN<CAS<ELA>>')) # elativus
        self.assertEqual(u'fiútól', affix(u'fiú', 'NOUN<CAS<ABL>>')) # ablativus
        self.assertEqual(u'fiún', affix(u'fiú', 'NOUN<CAS<SUE>>')) # superessivus
        self.assertEqual(u'fiúban', affix(u'fiú', 'NOUN<CAS<INE>>')) # inessivus
        self.assertEqual(u'fiúnál', affix(u'fiú', 'NOUN<CAS<ADE>>')) # adessivus
        self.assertEqual(u'fiúra', affix(u'fiú', 'NOUN<CAS<SBL>>')) # sublativus
        self.assertEqual(u'fiúba', affix(u'fiú', 'NOUN<CAS<ILL>>')) # illativus
        self.assertEqual(u'fiúhoz', affix(u'fiú', 'NOUN<CAS<ALL>>')) # allativus
        self.assertEqual(u'fiúig', affix(u'fiú', 'NOUN<CAS<TER>>')) # terminativus
        self.assertEqual(u'fiúval', affix(u'fiú', 'NOUN<CAS<INS>>')) # instrumentalis-comitativus
        self.assertEqual(u'fiúért', affix(u'fiú', 'NOUN<CAS<CAU>>')) # causalis-finalis
        self.assertEqual(u'fiúként', affix(u'fiú', 'NOUN<CAS<FOR>>')) # formativus
        self.assertEqual(u'fiúvá', affix(u'fiú', 'NOUN<CAS<TRA>>')) # translativus-factivus
        self.assertEqual(u'húsvétkor', affix(u'húsvét', 'NOUN<CAS<TEM>>')) # temporalis

        # fiúké fiú/NOUN<PLUR><ANP>
        # fiúéi fiú/NOUN<ANP<PLUR>>
        # fiúkéi fiú/NOUN<PLUR><ANP<PLUR>>
        # fiáéi fiú/NOUN<POSS><ANP<PLUR>>
        # fiaiéi fiú/NOUN<PLUR><POSS><ANP<PLUR>>
        # fiukéi fiú/NOUN<POSS<PLUR>><ANP<PLUR>>
        # fiaikéi fiú/NOUN<PLUR><POSS<PLUR>><ANP<PLUR>>
        # fiaitokéinak fiú/NOUN<PLUR><POSS<PLUR><2>><ANP<PLUR>><CAS<DAT>>
        # fiúék fiú/NOUN<PLUR<FAM>>
        # fiáék fiú/NOUN<PLUR<FAM>><POSS>
        # fiúéké fiú/NOUN<PLUR<FAM>><ANP>
        # fiáéké fiú/NOUN<PLUR<FAM>><POSS><ANP>

        # kiváncsijaitokét kivácsi/ADJ<PLUR><POSS<PLUR><2>><ANP><CAS<ACC>>
        # kétezreinkével kétezer/NUM<PLUR><POSS<PLUR><1>><ANP><CAS<INS>>

