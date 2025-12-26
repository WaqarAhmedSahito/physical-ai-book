import React from 'react';
import ChatPopup from './ChatPopup';

const LayoutWithChat = ({ children }) => {
  return (
    <div style={{ position: 'relative', minHeight: '100vh' }}>
      {children}
      <ChatPopup />
    </div>
  );
};

export default LayoutWithChat;