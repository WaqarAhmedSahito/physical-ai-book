import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatPopup from '@site/src/components/ChatPopup';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <ChatPopup />
    </>
  );
}