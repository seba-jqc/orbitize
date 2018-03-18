"""
Test the functionality of the API
"""
import numpy as np
import orbitize.lnlike as lnlike
import orbitize.system as system
import orbitize.read_input as read_input

def test_compute_model():
    """
    Test basic functionality of ``System.compute_model()``
    """
    data_table = read_input.read_formatted_file('test_val.csv')
    data_table['object'] = 1
    testSystem_parsing = system.System(
        1, data_table, 10., 10.
    )

    params_arr = np.array([[1.,0.,0.,0.,0.,245000.],[0.5,0.,0.,0.,0.,245000.]])

    model = testSystem_parsing.compute_model(params_arr)
    assert model.shape == (2,4,2)

def test_systeminit():
    """
    Test that initializing a ``System`` class produces a list of ``Prior``
    objects of the correct length when:
        - parallax and total mass are fixed
        - parallax and total mass errors are given
        - parallax is fixed, total mass error is given
        - parallax error is given, total mass error is fixed

    Test that the different types of data are parsed correctly
    when initializing a ``System`` object.
    """
    data_table = read_input.read_formatted_file('test_val.csv')

    # Manually set 'object' column of data table
    data_table['object'] = 1
    data_table['object'][1] = 2

    plx_mass_errs2lens = {
        (0.,0.): 12, 
        (1.,1.): 14, 
        (0.,1.): 13, 
        (1.,0.): 13
    }

    for plx_e, mass_e in plx_mass_errs2lens.keys():

        testSystem_priors = system.System(
            2, data_table, 10., 10., plx_err=plx_e, mass_err=mass_e
        )
        assert len(testSystem_priors.sys_priors) == \
            plx_mass_errs2lens[(plx_e, mass_e)]

    testSystem_parsing = system.System(
        2, data_table, 10., 10., 
        plx_err=0.5, mass_err=0.5
    )
    assert len(data_table[testSystem_parsing.seppa[0]]) == 0
    assert len(data_table[testSystem_parsing.seppa[1]]) == 1
    assert len(data_table[testSystem_parsing.seppa[2]]) == 1
    assert len(data_table[testSystem_parsing.radec[0]]) == 0
    assert len(data_table[testSystem_parsing.radec[1]]) == 1
    assert len(data_table[testSystem_parsing.radec[2]]) == 0


def test_chi2lnlike():
    """
    Test the ability of ``orbitize.lnlike.chi2_lnlike()`` 
    to work properly on arrays.
    """
    model = np.zeros((3,2,1))
    data=np.ones((2,1))
    errors=np.ones((2,1))

    chi2 = lnlike.chi2_lnlike(data, errors, model)
    assert chi2.all() == np.ones((3,2,1)).all()

def test_radec2seppa():
    """
    Basic test for convenience function converting RA/DEC to SEP/PA
    """
    ra = np.array([-1.,0.,-1.,1.])
    dec = np.array([0.,-1.,-1.,1.])
    sep, pa = system.radec2seppa(ra, dec)
    assert sep.all() == np.array([1.,1.,np.sqrt(2.),np.sqrt(2.)]).all()
    assert pa.all() == np.array([270.,180.,225.,45.]).all()




























