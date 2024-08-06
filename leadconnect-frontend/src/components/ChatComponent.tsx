import React, { useState, useEffect, useRef } from 'react'; // Importing necessary React hooks and libraries
import './../chat.css'; // Importing CSS file for styling
import { FaTimes, FaPlus, FaPaperPlane, FaRobot, FaUser } from "react-icons/fa"; // Importing FontAwesome icons
import axios from 'axios'; // Importing axios for making HTTP requests

type Contact = { // Defining the Contact type
    about: string;
    contact_url: string;
    current_location: string;
    experiences: Experience[];
    headline: string;
    name: string;
    profile_pic_url: string;
    frequency: string;
    last_interacted: string;
};

type Experience = { // Defining the Experience type
    bulletpoints: string;
    company_duration: string;
    company_location: string;
    company_name: string;
    company_role: string;
    company_total_duration: string;
};

type ChatComponentProps = { // Defining the props type for the ChatComponent
    contact: Contact;
};

const ChatComponent: React.FC<ChatComponentProps> = ({ contact }) => { // Defining the ChatComponent functional component
    const [message, setMessage] = useState(''); // Defining state for message input
    const [chatHistory, setChatHistory] = useState<{ text: string, time: string, sender: string }[]>([]); // Defining state for chat history
    const [chatVisible, setChatVisible] = useState(false); // Defining state for chat visibility
    const [modalVisible, setModalVisible] = useState(false); // Defining state for modal visibility
    const [loading, setLoading] = useState(false); // Defining state for loading indicator
    const chatBoxRef = useRef<HTMLDivElement>(null); // Creating a ref for the chat box
    const inputRef = useRef<HTMLInputElement>(null); // Creating a ref for the input field
    const chatBodyRef = useRef<HTMLDivElement>(null); // Creating a ref for the chat body

    useEffect(() => { // Using useEffect to handle component lifecycle
        const initialMessages = [ // Initial bot messages
            {
                text: 'Hi, Please wait I am contextualizing this chat with ' + contact.name + ' data.',
                time: new Date().toLocaleTimeString(),
                sender: 'bot'
            },
            {
                text: 'Below is the summary of that user.',
                time: new Date().toLocaleTimeString(),
                sender: 'bot'
            }
        ];

        const fetchData = async () => { // Function to fetch data from API
            setLoading(true); // Setting loading to true
            try {
                const experiences = contact.experiences.map(exp => exp.bulletpoints); // Extracting bulletpoints from experiences
                const response = await axios.post('http://localhost:5000/api/llm', { // Sending POST request to API
                    experiences,
                    initial_context: true
                });

                const fetchedMessages = [ // Bot messages after fetching data
                    {
                        text: response.data.customized_message,
                        time: new Date().toLocaleTimeString(),
                        sender: 'bot'
                    },
                    {
                        text: `<div>
    <p>You can ask below things to this person:</p>
    <ul style="list-style-type: disc; padding-left: 20px;">
        <li>Do you have any openings in your company?</li>
        <li>I have an interview in a few days in your company and need your guidance.</li>
        <li>Are you free for a coffee chat this month?</li>
        <li>I am trying to learn emerging technologies and your profile looks good. Can you guide me on how to start with my preparation?</li>
    </ul>
</div>`,
                        time: new Date().toLocaleTimeString(),
                        sender: 'bot'
                    }
                ];

                setChatHistory([...initialMessages, ...fetchedMessages]); // Updating chat history with initial and fetched messages
            } catch (error) {
                console.error('Error sending experiences:', error); // Logging error if API call fails
            } finally {
                setLoading(false); // Setting loading to false
            }
        };

        setChatHistory(initialMessages); // Setting initial chat history
        fetchData(); // Fetching data
    }, [contact.experiences]); // Dependency array for useEffect
    useEffect(() => {
        scrollToBottom(); // Scroll to bottom when chat history updates
    }, [chatHistory]);

    useEffect(() => { // Adding event listeners for clicks and key presses
        const handleClickOutside = (event: MouseEvent) => { // Handling clicks outside chat box
            if (chatBoxRef.current && !chatBoxRef.current.contains(event.target as Node)) {
                setChatVisible(false); // Hiding chat if click is outside chat box
            }
        };

        const handleEscKey = (event: KeyboardEvent) => { // Handling Escape key press
            if (event.key === 'Escape') {
                setChatVisible(false); // Hiding chat if Escape key is pressed
            }
        };

        const handleEnterKey = (event: KeyboardEvent) => { // Handling Enter key press
            if (event.key === 'Enter') {
                handleSendMessage(); // Sending message if Enter key is pressed
            }
        };

        document.addEventListener('mousedown', handleClickOutside); // Adding mousedown event listener
        document.addEventListener('keydown', handleEscKey); // Adding keydown event listener for Escape key

        document.addEventListener('enterkey', handleSendMessage); // Adding event listener for custom Enter key event

        if (inputRef.current) {
            inputRef.current.addEventListener('keydown', handleEnterKey); // Adding keydown event listener for Enter key to input field
        }

        return () => { // Cleanup function to remove event listeners
            document.removeEventListener('mousedown', handleClickOutside);
            document.removeEventListener('keydown', handleEscKey);

            if (inputRef.current) {
                inputRef.current.removeEventListener('keydown', handleEnterKey);
            }
        };
    }, [chatBoxRef, inputRef]);

    const scrollToBottom = () => { // Function to scroll chat to bottom
        if (chatBodyRef.current) {
            chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight; // Setting scroll position to bottom
        }
    };

    const handleSendMessage = async () => { // Function to handle sending messages
        if (message.trim()) { // Checking if message is not empty
            const currentTime = new Date().toLocaleTimeString(); // Getting current time
            const userMessage = { text: message, time: currentTime, sender: 'user' }; // Creating user message object
            setChatHistory(prevHistory => [...prevHistory, userMessage]); // Adding user message to chat history
            setMessage(''); // Clearing message input

            try {
                setLoading(true); // Setting loading to true

                const experiences = contact.experiences.map(exp => exp.bulletpoints); // Extracting bulletpoints from experiences
                const response = await axios.post('http://localhost:5000/api/llm', { // Sending POST request to API
                    experiences,
                    question: message,
                    initial_context: false
                });
                const botMessage = {
                    text: response.data.customized_message,
                    time: new Date().toLocaleTimeString(),
                    sender: 'bot'
                };
                setChatHistory(prevHistory => [...prevHistory, botMessage]); // Adding bot message to chat history
            } catch (error) {
                console.error('Error sending message:', error); // Logging error if API call fails
            } finally {
                setLoading(false); // Setting loading to false
            }
        }
    };

    const toggleChatVisibility = () => { // Function to toggle chat visibility
        setChatVisible(!chatVisible); // Toggling chatVisible state
    };

    const toggleModalVisibility = () => { // Function to toggle modal visibility
        setModalVisible(!modalVisible); // Toggling modalVisible state
    };

    return (
        <div className={`app-container ${chatVisible ? 'blur-background' : ''}`}> 
            <div className={`chat-box ${chatVisible ? 'visible' : ''}`} ref={chatBoxRef}> 
                <div className="chat-box-header">
                    <img src={contact.profile_pic_url} alt="profile" className="rounded-full avatar-chat" /> 
                    <span style={{ fontWeight: "bold", lineHeight: "2" }}> {chatVisible ? contact.name : ''}</span> 
                    <p id="addExtra" onClick={toggleChatVisibility}>
                        <span className="text-buttonBlue hover:text-blue-700"><FaTimes size={24} /></span> 
                    </p>
                </div>
                <div className="chat-box-body" ref={chatBodyRef}> 
                    {chatHistory.map((msg, index) => ( // Mapping over chat history to display messages
                        msg.text && (
                            <div key={index} className={`chat-box-body-${msg.sender === 'bot' ? 'receive' : 'send'}`}> 
                                <div dangerouslySetInnerHTML={{__html: msg.text.replace(/```html|```/g, '')}}/> 

                                <div style={{display: "flex", flexDirection: "row"}}>
                                    <span style={{
                                        fontSize: "14px",
                                        fontWeight: "bold",
                                        lineHeight: 1,
                                        display: "flex",
                                        flexDirection: "row",
                                        flex: "1"
                                    }}>{msg.sender === 'bot' ? <FaRobot className="chat-icon-receive"/> :
                                        <FaUser
                                            className="chat-icon-send"/>} {msg.sender === 'bot' ? 'Bot' : 'You'}</span> 
                                    <span>{msg.time}</span> 

                                </div>
                            </div>
                        )
                    ))}
                </div>
                {loading && ( // Loading indicator
                    <div className="dot-falling-container">
                        <div className="dot-falling"></div>
                    </div>
                )}
                <div className="chat-box-footer">
                    <button id="addExtra" onClick={toggleModalVisibility}>
                        <span className="text-buttonBlue hover:text-blue-700"><FaPlus size={24} /></span> 
                    </button>
                    <input
                        ref={inputRef}
                        placeholder="Type Here"
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)} // Updating message state on input change
                    />
                    <button id="addExtra" onClick={handleSendMessage}>
                        <span className="text-buttonBlue hover:text-blue-700"><FaPaperPlane size={24} /></span> 
                    </button>
                </div>
            </div>

            <div className="chat-button" onClick={toggleChatVisibility}
                style={{ display: chatVisible ? 'none' : 'flex' }}> 
                <img src={contact.profile_pic_url} alt="profile" className="rounded-full avatar-chat" /> 
                {contact.name} 
            </div>

            {modalVisible && ( // Conditional rendering of modal
                <div className="modal show-modal">
                    <div className="modal-content">
                        <span className="modal-close-button" onClick={toggleModalVisibility}>&times;</span> 
                        <h1>Add What you want here.</h1> 
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatComponent; // Exporting ChatComponent as default
