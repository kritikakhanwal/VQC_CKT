from qiskit.aqua.components.feature_maps import FeatureMap
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import BlueprintCircuit
import numpy as np
import matplotlib.pyplot as plt
import functools

from qiskit import BasicAer
from qiskit.circuit.library import ZFeatureMap,ZZFeatureMap, PauliFeatureMap
from qiskit.aqua import QuantumInstance
from qiskit.aqua.components.feature_maps import self_product
from qiskit.aqua.algorithms import QSVM
from qiskit.ml.datasets import ad_hoc_data
from numpy import pi
class CustomFeatureMap(FeatureMap):
    """Mapping data with a custom feature map."""
    
    def __init__(self, feature_dimension, depth=2, entangler_map=None):
        """
        Args:
            feature_dimension (int): number of features
            depth (int): the number of repeated circuits
            entangler_map (list[list]): describe the connectivity of qubits, each list describes
                                        [source, target], or None for full entanglement.
                                        Note that the order is the list is the order of
                                        applying the two-qubit gate.        
        """
        self._support_parameterized_circuit = False
        self._feature_dimension = feature_dimension
        self._num_qubits = self._feature_dimension = feature_dimension+1
        self._depth = depth
        self._entangler_map = None
        if self._entangler_map is None:
            self._entangler_map = [[i, j] for i in range(self._feature_dimension) for j in range(i + 1, self._feature_dimension)]
            
    def construct_circuit(self, x, qr, inverse=False):
        """Construct the feature map circuit.
        
        Args:
            x (numpy.ndarray): 1-D to-be-transformed data.
            qr (QauntumRegister): the QuantumRegister object for the circuit.
            inverse (bool): whether or not to invert the circuit.
            
        Returns:
            QuantumCircuit: a quantum circuit transforming data x.
        """
        qc1 = QuantumCircuit(4)

        
        for _ in range(self._depth):
            y = -1.3*x[0]+x[1]
            qc1.h(0)
            qc1.h(1)
            qc1.h(2)
            qc1.h(3)
            qc1.u1(x[0],0)
            qc1.u1(x[1],1)
            qc1.u1(x[2],2)
            qc1.u1(y,3)
            qc1.cx(0,1)
            qc1.u1((2*(pi-x[0])*(pi-x[1])),1)
            qc1.cx(0,1)
            qc1.cx(0,2)
            qc1.u1((2*(pi-x[0])*(pi-x[2])),2)
            qc1.cx(0,2)
            qc1.cx(0,3)
            qc1.u1((2*(pi-x[0])*(pi-y)),3)
            qc1.cx(0,3)
            qc1.cx(1,2)
            qc1.u1((2*(pi-x[1])*(pi-x[2])),2)
            qc1.cx(1,2)
            qc1.cx(1,3)
            qc1.u1((2*(pi-x[1])*(pi-y)),3)
            qc1.cx(1,3)
            qc1.cx(2,3)
            qc1.u1((2*(pi-x[2])*(pi-y)),3)
            qc1.cx(2,3)

            
            
            
        if inverse:
            qc1.inverse()
        return qc1
def feature_map():
    return CustomFeatureMap(feature_dimension=3, depth=2)
