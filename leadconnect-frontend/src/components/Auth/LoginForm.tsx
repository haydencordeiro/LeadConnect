import React, { useState } from 'react';
import { FaGithub } from 'react-icons/fa';
import SubmitButton from '../SubmitButton';
import ErrorMessage from '../ErrorMessage';

interface LoginFormProps {
  handleInputChange: (input: string, value: string) => void;
  handleSubmit: () => void;
  formData: {
    username: string;
    password: string;
  };
  errorMessage: string;
}

const LoginForm: React.FC<LoginFormProps> = ({ handleInputChange, handleSubmit, formData,errorMessage }) => {
  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSubmit();
  };

  return (
    <form onSubmit={onSubmit} className="flex flex-col">
      {/* <button type="button" className="flex items-center justify-center mb-4 p-2 border rounded bg-gray-800 text-white rounded-lg shadow-lg">
        <FaGithub className="mr-2" /> Login with GitHub
      </button> */}
      <input
        type="text"
        value={formData.username}
        onChange={(e) => handleInputChange('username', e.target.value)}
        placeholder="Username"
        className="mb-4 p-2 border rounded"
        required
      />
      <input
        type="password"
        value={formData.password}
        onChange={(e) => handleInputChange('password', e.target.value)}
        placeholder="Password"
        className="mb-4 p-2 border rounded"
        required
      />
      {errorMessage && <ErrorMessage message={errorMessage} />}
      <SubmitButton type="Login" />
      <p className="text-sm text-gray-600 mt-4">
        By signing in, you accept all terms & conditions and privacy policies.
      </p>
    </form>
  );
};

export default LoginForm;
