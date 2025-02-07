import React from 'react';
import PropTypes from 'prop-types';

export const Dialog = ({ open, onOpenChange, children }) => {
  return (
    <div>
      {open && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
          onClick={() => onOpenChange(false)}
        >
          <div
            className="bg-white rounded-lg shadow-lg max-w-lg w-full"
            onClick={(e) => e.stopPropagation()}
          >
            {children}
          </div>
        </div>
      )}
    </div>
  );
};

export const DialogTrigger = ({ asChild, children, onClick }) => {
  const Child = asChild ? React.cloneElement(children, { onClick }) : <button onClick={onClick}>{children}</button>;
  return <>{Child}</>;
};

export const DialogContent = ({ children }) => (
  <div className="p-4">{children}</div>
);

export const DialogHeader = ({ children }) => (
  <div className="p-4 border-b">{children}</div>
);

export const DialogTitle = ({ children }) => (
  <h2 className="text-lg font-bold">{children}</h2>
);

Dialog.propTypes = {
  open: PropTypes.bool.isRequired,
  onOpenChange: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired,
};

DialogTrigger.propTypes = {
  asChild: PropTypes.bool,
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func,
};

DialogContent.propTypes = {
  children: PropTypes.node.isRequired,
};

DialogHeader.propTypes = {
  children: PropTypes.node.isRequired,
};

DialogTitle.propTypes = {
  children: PropTypes.node.isRequired,
};