from random import randint

from apprentice.working_memory import ExpertaWorkingMemory
from apprentice.working_memory.adapters.experta_.factory import \
    ExpertaSkillFactory
from apprentice.working_memory.representation import Sai
from experta import Rule, Fact, W, KnowledgeEngine, MATCH, TEST, AS, NOT

max_depth = 1


def is_numeric_str(x):
    try:
        x = float(x)
        return True
    except Exception:
        return False


class EmptyAdditionEngine(KnowledgeEngine):
    sais = []


class AdditionEngine(KnowledgeEngine):
    sais = []

    @Rule(
        Fact(id='done')
    )
    def click_done(self):
        print("FIRED CLICK DONE")
        return Sai(selection='done',
                   action='ButtonPressed',
                   # input={'value': -1})
                   input={'value': '-1'})

    @Rule(
        Fact(id=MATCH.field_id, contentEditable=True, value=MATCH.value)
    )
    def check(self, field_id):
        print("FIRED CHECK")
        return Sai(selection=field_id,
                   action='UpdateTextArea',
                   input={'value': "x"})

    @Rule(
        Fact(id=W(), contentEditable=False, value=MATCH.value),
        TEST(lambda value_from: value_from != ""),
        Fact(id=MATCH.field_id, contentEditable=True, value=W()))
    def update_field(self, field_id, value):
        #print("FIRED UPDATE FIELD")
        s = Sai(selection=field_id,
                action='UpdateTextField',
                # action='UpdateTextArea',
                input={'value': value})
        if int(value) == 3:
            self.sais.append(s)
        return s

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, contentEditable=False,
                         value=MATCH.value1),
        TEST(lambda fact1: 'depth' not in fact1 or fact1['depth'] < max_depth),
        TEST(lambda value1: str(value1).isnumeric()),
        AS.fact2 << Fact(id=MATCH.id2, contentEditable=False,
                         value=MATCH.value2),
        TEST(lambda id1, id2: id1 <= id2),
        TEST(lambda fact2: 'depth' not in fact2 or fact2['depth'] < max_depth),
        TEST(lambda value2: str(value2).isnumeric()),
        NOT(Fact(operator='add', ele1=MATCH.id1, ele2=MATCH.id2))
    )
    def add(self, id1, value1, fact1, id2, value2, fact2):
        #print("FIRED ADD")
        new_id = 'add(%s, %s)' % (id1, id2)

        new_value = float(value1) + float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        depth1 = 0 if 'depth' not in fact1 else fact1['depth']
        depth2 = 0 if 'depth' not in fact2 else fact2['depth']
        new_depth = 1 + max(depth1, depth2)

        self.declare(Fact(id=new_id,
                          operator='add',
                          ele1=id1,
                          ele2=id2,
                          contentEditable=False,
                          value=new_value,
                          depth=new_depth))


class FractionsEngine(KnowledgeEngine):

    @Rule(
        Fact(id='done')
    )
    def click_done(self):
        return Sai(selection='done',
                   action='ButtonPressed',
                   input={'value': -1})
        # input={'value': '-1'})

    @Rule(
        Fact(id=MATCH.field_id, contentEditable=True, value=MATCH.value)
    )
    def check(self, field_id):
        return Sai(selection=field_id,
                   action='UpdateTextArea',
                   input={'value': "x"})

    @Rule(
        Fact(id=W(), contentEditable=False, value=MATCH.value),
        TEST(lambda value_from: value_from != ""),
        Fact(id=MATCH.field_id, contentEditable=True, value=W()))
    def update_field(self, field_id, value):
        return Sai(selection=field_id,
                   # action='UpdateTextField',
                   action='UpdateTextArea',
                   input={'value': value})

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, contentEditable=False,
                         value=MATCH.value1),
        TEST(lambda fact1: 'depth' not in fact1 or fact1['depth'] < max_depth),
        TEST(lambda value1: is_numeric_str(value1)),
        AS.fact2 << Fact(id=MATCH.id2, contentEditable=False,
                         value=MATCH.value2),
        TEST(lambda id1, id2: id1 <= id2),
        TEST(lambda fact2: 'depth' not in fact2 or fact2['depth'] < max_depth),
        TEST(lambda value2: is_numeric_str(value2)),
        NOT(Fact(operator='add', ele1=MATCH.id1, ele2=MATCH.id2))
    )
    def add(self, id1, value1, fact1, id2, value2, fact2):
        new_id = 'add(%s, %s)' % (id1, id2)

        new_value = float(value1) + float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        depth1 = 0 if 'depth' not in fact1 else fact1['depth']
        depth2 = 0 if 'depth' not in fact2 else fact2['depth']
        new_depth = 1 + max(depth1, depth2)

        self.declare(Fact(id=new_id,
                          operator='add',
                          ele1=id1,
                          ele2=id2,
                          contentEditable=False,
                          value=new_value,
                          depth=new_depth))

    @Rule(
        AS.fact1 << Fact(id=MATCH.id1, contentEditable=False,
                         value=MATCH.value1),
        TEST(lambda fact1: 'depth' not in fact1 or fact1['depth'] < max_depth),
        TEST(lambda value1: is_numeric_str(value1)),
        AS.fact2 << Fact(id=MATCH.id2, contentEditable=False,
                         value=MATCH.value2),
        TEST(lambda id1, id2: id1 <= id2),
        TEST(lambda fact2: 'depth' not in fact2 or fact2['depth'] < max_depth),
        TEST(lambda value2: is_numeric_str(value2)),
        NOT(Fact(operator='multiply', ele1=MATCH.id1, ele2=MATCH.id2))
    )
    def multiply(self, id1, value1, fact1, id2, value2, fact2):
        new_id = 'multiply(%s, %s)' % (id1, id2)

        new_value = float(value1) * float(value2)
        if new_value.is_integer():
            new_value = int(new_value)
        new_value = str(new_value)

        depth1 = 0 if 'depth' not in fact1 else fact1['depth']
        depth2 = 0 if 'depth' not in fact2 else fact2['depth']
        new_depth = 1 + max(depth1, depth2)

        self.declare(Fact(id=new_id,
                          operator='multiply',
                          ele1=id1,
                          ele2=id2,
                          contentEditable=False,
                          value=new_value,
                          depth=new_depth))


ke = FractionsEngine()
skill_factory = ExpertaSkillFactory(ke)
click_done_skill = skill_factory.from_ex_rule(ke.click_done)
check_skill = skill_factory.from_ex_rule(ke.check)
update_field_skill = skill_factory.from_ex_rule(ke.update_field)
add_skill = skill_factory.from_ex_rule(ke.add)
multiply_skill = skill_factory.from_ex_rule(ke.multiply)
fraction_skill_set = {'click_done': click_done_skill, 'check': check_skill,
                      'update': update_field_skill, 'add': add_skill,
                      'multiply': multiply_skill}


class RandomFracEngine(KnowledgeEngine):
    @Rule(
        Fact(id=MATCH.id, contentEditable=True, value=W())
    )
    def input_random(self, id):
        return Sai(selection=id, action='UpdateTextArea',
                   input={'value': str(randint(0, 100))})

    @Rule(
        Fact(id='done')
    )
    def click_done(self):
        return Sai(selection='done', action='ButtonPressed',
                   input={'value': -1})


def fact_from_dict(f):
    if '__class__' in f:
        fact_class = f['__class__']
    else:
        fact_class = Fact
    f2 = {k: v for k, v in f.items() if k[:2] != "__"}
    return fact_class(f2)


if __name__ == "__main__":
    from apprentice.explain.explanation import Explanation
    import inspect

    engine = AdditionEngine()

    engine.reset()

    f1 = Fact(id='JCommTable.R0C0', value='1', contentEditable=False)
    f2 = Fact(id='JCommTable.R1C0', value='2', contentEditable=False)
    f3 = Fact(id='JCommTable.R1C1', contentEditable=True, value='')

    engine.declare(f1)
    engine.declare(f2)
    engine.declare(f3)
    engine.run(10)
    sais = engine.sais

    print("===")
    ex = Explanation(engine.sais[0])
    nr = ex.new_rule
    print(nr)

    new_wm = ExpertaWorkingMemory(EmptyAdditionEngine())
    print(ex.general)
    # generate a new rule and assign it to the blank working memory
    print(inspect.signature(nr))
    new_wm.add_rule(nr)

    new_wm.ke.declare(f1)
    new_wm.ke.declare(f2)
    new_wm.ke.declare(f3)
    # test that the new rule fires correctly
    new_wm.ke.run(10)

    assert new_wm.ke.sais[0] == Sai(selection='JCommTable.R1C1',
                                    action='UpdateTextField',
                                    input={'value': '3'})
