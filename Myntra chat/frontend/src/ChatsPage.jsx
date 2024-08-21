import React from 'react';
import { PrettyChatWindow } from "react-chat-engine-pretty";
import { FaShoppingCart } from 'react-icons/fa';

const ChatsPage = (props) => {
const handleCartClick = () => {
  window.location.href = 'file:///C:/Users/hp/Desktop/myntra_changes/homepage.html';
};

  return (
    <div className="background">
      <div className="chat-wrapper">
        <PrettyChatWindow
          projectId={import.meta.env.VITE_CHAT_ENGINE_PROJECT_ID}
          username={props.user.username}
          secret={props.user.secret}
        />
        <div className="icon-container">
          <FaShoppingCart className="chat-icon" onClick={handleCartClick} />
        </div>
      </div>
    </div>
  );
};

export default ChatsPage;
