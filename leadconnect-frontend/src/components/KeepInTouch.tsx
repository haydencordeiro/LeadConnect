import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable, DropResult, DraggableProvided, DraggableStateSnapshot, DroppableProvided, DroppableStateSnapshot } from '@hello-pangea/dnd';
import axios from 'axios';
import { Contact } from '../types'; // Import the shared Contact type

type ContactWithInitial = Contact & {
  initial: string;
};

type ContactsState = {
  Weekly: ContactWithInitial[];
  Biweekly: ContactWithInitial[];
  Monthly: ContactWithInitial[];
  Bimonthly: ContactWithInitial[];
  Once_in_3_months: ContactWithInitial[];
  Once_in_6_months: ContactWithInitial[];
};

const categorizeContacts = (contacts: Contact[]): ContactsState => {
  const categorizedContacts: ContactsState = {
    Weekly: [],
    Biweekly: [],
    Monthly: [],
    Bimonthly: [],
    Once_in_3_months: [],
    Once_in_6_months: [],
  };

  contacts.forEach(contact => {
    const initial = contact.name.charAt(0);
    const categorizedContact: ContactWithInitial = { ...contact, initial };

    switch (contact.frequency) {
      case 'Weekly':
        categorizedContacts.Weekly.push(categorizedContact);
        break;
      case 'Biweekly':
        categorizedContacts.Biweekly.push(categorizedContact);
        break;
      case 'Monthly':
        categorizedContacts.Monthly.push(categorizedContact);
        break;
      case 'Bimonthly':
        categorizedContacts.Bimonthly.push(categorizedContact);
        break;
      case 'Once_in_3_months':
        categorizedContacts.Once_in_3_months.push(categorizedContact);
        break;
      case 'Once_in_6_months':
        categorizedContacts.Once_in_6_months.push(categorizedContact);
        break;
      // default:
      //   categorizedContacts.Weekly.push(categorizedContact);
      //   break;
    }
  });

  return categorizedContacts;
};

type KeepInTouchProps = {
  contacts: Contact[];
};

const KeepInTouch: React.FC<KeepInTouchProps> = ({ contacts }) => {
  const [categorizedContacts, setCategorizedContacts] = useState<ContactsState>(() =>
    categorizeContacts(contacts)
  );

  useEffect(() => {
    setCategorizedContacts(categorizeContacts(contacts));
  }, [contacts]);

  const updateContactFrequency = async (contact: ContactWithInitial, newFrequency: string) => {
    try {
        // Step 1: Make a GET request to fetch the contact URL
        const getUrl = `http://127.0.0.1:5000/api/contacts/contact_url/${contact.name}`;
        console.log('Fetching contact URL from:', getUrl);
        const response = await axios.get(getUrl);
        console.log(response.data)
        // Step 2: Log the contact URL
        const contactUrl = response.data.contact_url;
        console.log('Contact URL:', contactUrl);

      // Step 3: Use the contact URL to make the PUT request
      const updateUrl = 'http://127.0.0.1:5000/api/connections/frequency';
      const updateResponse = await fetch(updateUrl, {
          method: 'PUT',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `${localStorage.getItem('token')}`, // Include token if necessary
          },
          body: JSON.stringify({
              contact_url: contactUrl,
              frequency: newFrequency,
          }),
      });

      if (updateResponse.ok) {
          console.log('Successfully updated contact frequency');
      } else {
          console.error('Failed to update contact frequency', await updateResponse.json());
      }
    } catch (error) {
        console.error('Failed to update contact frequency', error);
    }
};


  
  

  const onDragEnd = (result: DropResult) => {
    const { source, destination } = result;

    if (!destination) return;

    if (source.droppableId === destination.droppableId && source.index === destination.index) return;

    const sourceList = Array.from(categorizedContacts[source.droppableId as keyof ContactsState]);
    const [movedItem] = sourceList.splice(source.index, 1);

    const destinationList = Array.from(categorizedContacts[destination.droppableId as keyof ContactsState]);
    destinationList.splice(destination.index, 0, movedItem);

    setCategorizedContacts({
      ...categorizedContacts,
      [source.droppableId]: sourceList,
      [destination.droppableId]: destinationList,
    });

    // Update the contact frequency in the backend
    const newFrequency = destination.droppableId.replace(/([a-z])([A-Z])/g, '$1 $2');
    console.log('New frequency:', newFrequency);
    updateContactFrequency(movedItem, newFrequency);
  };

  return (
    <div className='p-6'>
      <h1 className='text-3xl font-bold mb-4'>Keep In Touch</h1>
      <p className='mb-6'>Set a frequency to reach out and build stronger relationships</p>
      <div className='mb-4'>
        <select className='p-2 border-slate-200 border-[1px] rounded'>
          <option>All Contacts</option>
        </select>
      </div>
      <DragDropContext onDragEnd={onDragEnd}>
        <div className='grid grid-cols-1 md:grid-cols-6 gap-4'>
          {Object.keys(categorizedContacts).map((key) => (
            <Droppable droppableId={key} key={key}>
              {(provided: DroppableProvided, snapshot: DroppableStateSnapshot) => (
                <div
                  className={`border-slate-200 border-[1px] p-2 rounded ${snapshot.isDraggingOver ? 'bg-blue-100' : 'bg-white'}`}
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                >
                  <h2 className='font-bold mb-2'>
                    {key.replace(/([a-z])([A-Z])/g, '$1 $2')}
                  </h2>
                  {categorizedContacts[key as keyof ContactsState].map((contact, index) => (
                    <Draggable
                      draggableId={contact.name}
                      index={index}
                      key={contact.name}
                    >
                      {(provided: DraggableProvided, snapshot: DraggableStateSnapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className={`flex items-center mb-2 p-2 border rounded ${snapshot.isDragging ? 'bg-blue-50' : 'bg-white'}`}
                        >
                          <div className='bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center mr-2'>
                            {contact.initial}
                          </div>
                          {contact.name}
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
};

export default KeepInTouch;
