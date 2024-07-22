import { MagnifyingGlassIcon } from '@heroicons/react/20/solid'
import { useState } from 'react'

export function Search() {
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [day, setDay] = useState('');

  const handleSearch = () => {
    console.log('Search clicked:', { year, month, day });
    // Add your search logic here
  };

  const max_year = new Date().getFullYear();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 animate-gradient-x"></div>
      <div className="w-full max-w-md p-4 space-y-4 bg-white bg-opacity-80 dark:bg-gray-700 dark:bg-opacity-80 rounded-lg shadow-md relative z-10">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-full">
            <label htmlFor="year" className="block text-sm font-medium text-gray-700 dark:text-gray-200">
              Year
            </label>
            <input
              type="number"
              id="year"
              name="year"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              min="2023"
              max={max_year}
              className="mt-1 block w-full rounded-md border-gray-300 py-2 px-3 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-600 dark:text-white"
              placeholder="YYYY"
            />
          </div>
          <div className="w-full">
            <label htmlFor="month" className="block text-sm font-medium text-gray-700 dark:text-gray-200">
              Month
            </label>
            <input
              type="number"
              id="month"
              name="month"
              min="1"
              max="12"
              value={month}
              onChange={(e) => setMonth(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 py-2 px-3 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-600 dark:text-white"
              placeholder="MM"
            />
          </div>
          <div className="w-full">
            <label htmlFor="day" className="block text-sm font-medium text-gray-700 dark:text-gray-200">
              Day
            </label>
            <input
              type="number"
              id="day"
              name="day"
              min="1"
              max="31"
              value={day}
              onChange={(e) => setDay(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 py-2 px-3 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-600 dark:text-white"
              placeholder="DD"
            />
          </div>
        </div>
        <div className="relative my-4">
          <div aria-hidden="true" className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300 dark:border-gray-600" />
          </div>
          <div className="relative flex justify-center">
            <button
              id="search_button"
              type="button"
              onClick={handleSearch}
              className="inline-flex items-center gap-x-1.5 rounded-full bg-white px-3 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 dark:bg-gray-600 dark:text-white dark:ring-gray-500 dark:hover:bg-gray-500"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-500 dark:text-gray-300">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
              Search
            </button>
          </div>
        </div>
      </div>
      <style>{`
        @keyframes gradient-x {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .animate-gradient-x {
          background-size: 400% 400%;
          animation: gradient-x 15s ease infinite;
        }
      `}</style>
    </div>
  );
}