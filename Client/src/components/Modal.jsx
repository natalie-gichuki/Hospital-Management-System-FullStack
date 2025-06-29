// src/components/Modal.jsx
import React from 'react';

const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50">
      <div className="bg-white rounded-lg p-6 shadow-md w-96">
        <button className="float-right text-red-500" onClick={onClose}>×</button>
        <div>{children}</div>
      </div>
    </div>
  );
};

export default Modal;
