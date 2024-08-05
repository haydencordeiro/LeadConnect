import React, {useEffect, useState} from 'react';
import {FaSort, FaFilter, FaStickyNote, FaTrash, FaSearch, FaLinkedin, FaRobot} from 'react-icons/fa';
import {Contact} from '../types'; // Import the shared types
import ContactModal from './AddContact';
import NotesPopup from './NotesPopup';
import ChatComponent from './ChatComponent';
import InDepthContactInfo from './InDepthContactInfo';
import GenericChatComponent from "./GenericChatComponent.tsx";

type MainTableProps = {
    contacts: Contact[];
    setContacts?: React.Dispatch<React.SetStateAction<Contact[]>>; // Optional prop
    token: string | null;
    deleteContact: (url: string) => void;
};

const MainTable: React.FC<MainTableProps> = ({contacts, setContacts, token, deleteContact}) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedContact, setSelectedContact] = useState<Contact | null>(null);
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const [filterDropdownVisible, setFilterDropdownVisible] = useState(false);
    const [filterValues, setFilterValues] = useState({
        name: '',
        role: '',
        frequency: '',
        last_interacted: ''
    });
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedContacts, setSelectedContacts] = useState<Set<string>>(new Set());
    const [showChat, setShowChat] = useState(false);
    const [currentContact, setCurrentContact] = useState<Contact | null>(null);
    const [showInDepthContactInfo, setShowInDepthContactInfo] = useState(false);
    const [selectedInDepthContact, setSelectedInDepthContact] = useState<Contact | null>(null);
    const [encodedData, setEncodedData] = useState('');


    useEffect(() => {
        const hash = window.location.hash;
        const queryString = hash.includes('?') ? hash.split('?')[1] : '';
        const urlParams = new URLSearchParams(queryString);
        const encodedDatad = urlParams.get('query');
        const encodedData = encodedDatad?.replace(/(-)+/g, ' ');
        if (encodedData) {
            try {
                setEncodedData(encodedData);
            } catch (error) {
                console.error('Error decoding data:', error);
            }
        }
    }, []);

    const handleDeleteContact = async (url: string) => {
        deleteContact(url);
        try {
            const response = await fetch('http://localhost:5000/api/createcontact', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `${token}`,
                },
                body: JSON.stringify({
                    linkedinURL: url
                }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
        } catch (err: unknown) {
            if (err instanceof Error) {
                // setError(err.message);
            } else {
                // setError('An unknown error occurred');
            }
        }
    };

    const handleNotesClick = (contact: Contact) => {
        setSelectedContact(contact);
    };

    const handleIconClick = (icon: string) => {
        alert(`You clicked on the ${icon} icon!`);
    };

    const handleOpenChat = (contact: Contact) => {
        setCurrentContact(contact);
        setShowChat(true);
    };

    const handleSort = () => {
        const sortedContacts = [...contacts].sort((a, b) => {
            const dateA = new Date(a.last_interacted).getTime();
            const dateB = new Date(b.last_interacted).getTime();
            return sortOrder === 'asc' ? dateA - dateB : dateB - dateA;
        });
        if (setContacts) {
            setContacts(sortedContacts);
        }
        setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    };

    const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFilterValues({...filterValues, [name]: value});
    };

    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(e.target.value);
    };

    const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.checked) {
            setSelectedContacts(new Set(contacts.map(contact => contact.name)));
        } else {
            setSelectedContacts(new Set());
        }
    };

    const handleSelectContact = (contactName: string) => {
        setShowInDepthContactInfo(false);
        const newSelectedContacts = new Set(selectedContacts);
        if (newSelectedContacts.has(contactName)) {
            newSelectedContacts.delete(contactName);
        } else {
            newSelectedContacts.add(contactName);
        }
        setSelectedContacts(newSelectedContacts);
    };

    const handleShowInDepthContactInfo = (contact: Contact) => {
        setSelectedInDepthContact(contact);
        setShowInDepthContactInfo(true);
    };

    const filteredContacts = contacts.filter(contact => {
        return (
            contact.name.toLowerCase().includes(filterValues.name.toLowerCase()) &&
            contact.experiences[0].company_role.toLowerCase().includes(filterValues.role.toLowerCase()) &&
            contact.frequency.toLowerCase().includes(filterValues.frequency.toLowerCase()) &&
            contact.last_interacted.toLowerCase().includes(filterValues.last_interacted.toLowerCase())
        );
    });

    const searchFilteredContacts = filteredContacts.filter(contact =>
        contact.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="h-[89%] p-1 bg-cardWhite flex flex-col relative">
            <div className="ml-4 mr-3 flex justify-between items-center mb-4 sticky top-0 bg-cardWhite z-10">
                <div>
                    <h2 className="text-2xl opacity-75 font-bold color-secondaryTextColor">All contacts</h2>
                    <p className="text-lg color-secondaryTextColor">{searchFilteredContacts.length} total contacts</p>
                </div>
                {encodedData && <GenericChatComponent contacts={searchFilteredContacts}/>}
                {/*<button*/}
                {/*    className="bg-buttonBlue text-cardWhite px-3 py-2 rounded-lg hover:bg-blue-600"*/}
                {/*    onClick={() => setIsModalOpen(true)}*/}
                {/*>*/}
                {/*    + Add new contact*/}
                {/*</button>*/}
            </div>
            <div
                className="flex justify-between items-center bg-cardWhite p-1 rounded-lg mb-4 mr-16 sticky top-16 z-10"
                style={{zIndex: 1}}>
                <div className="ml-3 flex items-center space-x-4">
                    <input
                        type="checkbox"
                        className="form-checkbox h-4 w-4 text-buttonBlue"
                        onChange={handleSelectAll}
                        checked={selectedContacts.size === contacts.length}
                    />
                    <span className="text-lg opacity-85 color-secondaryTextColor">Select all</span>
                </div>
                <div className="flex items-center space-x-4 relative">
                    <button
                        className="bg-cardWhite opacity-85 color-secondaryTextColor px-4 py-2 rounded-lg border-slate-200 border-[1px] hover:bg-gray-300">
                        Properties
                    </button>
                    <button onClick={handleSort}
                            className="bg-cardWhite opacity-85 color-secondaryTextColor px-4 py-2 rounded-lg flex items-center border-slate-200 border-[1px] hover:bg-gray-300">
                        <span className="mr-2"><FaSort/></span> Sort
                    </button>
                    <button
                        onClick={() => setFilterDropdownVisible(!filterDropdownVisible)}
                        className="bg-cardWhite opacity-85 color-secondaryTextColor px-4 py-2 rounded-lg flex items-center border-slate-200 border-[1px] hover:bg-gray-300"
                    >
                        <span className="mr-2"><FaFilter/></span> Filter
                    </button>
                    <div className="relative flex items-center">
            <span className="absolute left-3 text-gray-400">
              <FaSearch/>
            </span>
                        <input
                            type="text"
                            placeholder="Search contact..."
                            value={searchTerm}
                            onChange={handleSearchChange}
                            className="border border-gray-300 pl-10 pr-6 py-2 rounded-lg opacity-55 bg-searchBarBackground"
                        />
                    </div>
                </div>

            </div>

            {filterDropdownVisible && (
                <div className="fixed inset-0 z-40 flex justify-end">
                    <div className="fixed inset-0 bg-black bg-opacity-50"
                         onClick={() => setFilterDropdownVisible(false)}></div>
                    <div className="relative bg-white w-64 h-full z-50 p-4">
                        <h3 className="text-xl font-semibold mb-4">Filter Contacts</h3>
                        <div className="flex flex-col space-y-4">
                            <input
                                type="text"
                                name="name"
                                placeholder="Filter by name"
                                value={filterValues.name}
                                onChange={handleFilterChange}
                                className="border border-gray-300 p-2 rounded-lg"
                            />
                            <input
                                type="text"
                                name="role"
                                placeholder="Filter by role"
                                value={filterValues.role}
                                onChange={handleFilterChange}
                                className="border border-gray-300 p-2 rounded-lg"
                            />
                            <input
                                type="text"
                                name="frequency"
                                placeholder="Filter by frequency"
                                value={filterValues.frequency}
                                onChange={handleFilterChange}
                                className="border border-gray-300 p-2 rounded-lg"
                            />
                            <input
                                type="text"
                                name="date"
                                placeholder="Filter by date"
                                value={filterValues.last_interacted}
                                onChange={handleFilterChange}
                                className="border border-gray-300 p-2 rounded-lg"
                            />
                            <button
                                onClick={() => setFilterDropdownVisible(false)}
                                className="bg-buttonBlue text-cardWhite px-4 py-2 rounded-lg hover:bg-blue-600 mt-4"
                            >
                                Apply Filters
                            </button>
                        </div>
                    </div>
                </div>
            )}

<div className="flex-grow overflow-hidden">
                <div className="bg-cardWhite rounded-lg overflow-y-auto scrollbar-thin h-full">
                    {searchFilteredContacts.map((contact, index) => (
                        <div key={index}
                             className="grid grid-cols-12 gap-4 px-4 py-2 border-b border-gray-100 hover:border-l-4 hover:border-l-blue-400 hover:bg-highlightBlue items-center">
                            <div className="col-span-7 flex items-center space-x-4 whitespace-nowrap">
                                <input
                                    type="checkbox"
                                    className="form-checkbox h-4 w-4 text-buttonBlue"
                                    onChange={() => handleSelectContact(contact.name)}
                                    checked={selectedContacts.has(contact.name)}
                                />
                                <img src={contact.profile_pic_url} alt="profile" className="w-10 h-10 rounded-full"/>
                                <div className="flex items-center">
                                    <p
                                        className="font-semibold text-lg opacity-80 cursor-pointer"
                                        onClick={() => handleShowInDepthContactInfo(contact)}
                                    >
                                        {contact.name}
                                    </p>
                                    <p className="text-lg opacity-60 ml-2">{contact.experiences[0].company_role}</p>
                                </div>
                            </div>
                            <div className="col-span-2 text-lg opacity-80">{contact.frequency}</div>
                            <div className="col-span-2 flex space-x-1">
                                <button onClick={() => handleNotesClick(contact)}
                                        className="bg-highlightBlue text-buttonBlue px-2 py-2 rounded-full transition duration-300 ease-in-out">
                                    <span className="text-buttonBlue hover:text-blue-700"><FaStickyNote/></span>
                                </button>
                                <a href={`${contact.contact_url}`} target="_blank" rel="noopener noreferrer">
                                    <button
                                        className="bg-highlightBlue text-buttonBlue px-2 py-2 rounded-full transition duration-300 ease-in-out">
                                        <span className="text-buttonBlue hover:text-blue-700"><FaLinkedin/></span>
                                    </button>
                                </a>
                                <button onClick={() => handleOpenChat(contact)}
                                        className="bg-highlightBlue text-buttonBlue px-2 py-2 rounded-full transition duration-300 ease-in-out">
                                    <span className="text-buttonBlue hover:text-blue-700"><FaRobot/></span>
                                </button>
                                <button onClick={() => handleDeleteContact(contact.contact_url)}
                                        className="bg-highlightBlue text-buttonBlue px-2 py-2 rounded-full transition duration-300 ease-in-out">
                                    <span className="text-buttonBlue hover:text-blue-700"><FaTrash/></span>
                                </button>
                            </div>
                            <div className="col-span-1 text-lg opacity-60">{contact.last_interacted}</div>
                        </div>
                    ))}
                </div>
            </div>
            {showChat && currentContact && <ChatComponent contact={currentContact}/>}

            {selectedContact && <NotesPopup contactName={selectedContact.name} onClose={() => setSelectedContact(null)}
                                            contactUrl={selectedContact.contact_url}
                                            initialNote={selectedContact.notes || ''} token={token}/>}
            {showInDepthContactInfo && selectedInDepthContact && (
                <InDepthContactInfo
                    contact={selectedInDepthContact}
                    onClose={() => setShowInDepthContactInfo(false)}
                />
            )}
        </div>
    );
};

export default MainTable;
