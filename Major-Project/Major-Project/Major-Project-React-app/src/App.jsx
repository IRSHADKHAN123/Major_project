import React, { useState } from 'react';
// import './App.css'
function App() {
  const [ciphertext, setCiphertext] = useState('');
  const [response, setResponse] = useState(null);
  const [loading,setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true)
    const res = await fetch(`http://127.0.0.1:5000/ciphertype?ciphertext=${ciphertext}`);
    const data = await res.json();
    setResponse(data);
    setLoading(false)
  };

  return (
    <div className="flex justify-center items-center h-screen bg-slate-900 text-slate-300">
    <div className='fixed top-[50px] text-xl'>Cipher Type Classifier</div>
      <div className="bg-slate-900 rounded-lg p-8 fixed top-[100px]">
        <form onSubmit={handleSubmit} className="flex flex-col items-center">
          <textarea
            type="text"
            name="ciphertext"
            value={ciphertext}
            onChange={(e) => setCiphertext(e.target.value)}
            placeholder="Enter ciphertext"
            className="block mb-4 px-4 py-2 border border-gray-300 w-[500px] rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-800  overflow-hidden"
          />
          <button
            type="submit"
            className="bg-slate-800 hover:bg-blue-700  font-bold py-2 px-4 rounded ml-auto"
          >
            Predict Cipher
          </button>
        </form>
        {loading  && <p>Loading...</p>}
        {response && !loading && (
          <table className="mt-8 w-full">
            <thead>
              <tr>
                <th className="px-4 py-2 border">Model Name</th>
                <th className="px-4 py-2 border">Predicted Cipher Type</th>
                <th className="px-4 py-2 border">Probability</th>
              </tr>
            </thead>
            <tbody>
              {response.map((item, index) => (
                <tr key={index}>
                  <td className="px-4 py-2 border">{item.model_name}</td>
                  <td className="px-4 py-2 border">{item.cipher_type.join(', ')}</td>
                  <td className="px-4 py-2 border">{item.probability}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;