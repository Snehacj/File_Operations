import mro

def test_process_order(capsys):
    obj=mro.D()
    obj.process()

    captured=capsys.readouterr().out.strip().split("\n")

    expected=[
        "D.process() called",
        "B.process() called",
        "C.process() called",
        "A.process() called",
    
    ]

    assert captured==expected,f"Output mismatch. Got {captured}"


def test_mro_structure():
    expected_mro=[
        mro.D,
        mro.B,
        mro.C,
        mro.A,
        object
    ]

    assert mro.D.mro() == expected_mro