import React, { useState, useEffect, useContext } from "react";
import { projectAuth, projectFirestore } from "./firebase";

const AppContext = React.createContext();

const AppProvider = ({ children }) => {
  const [stopwatch, setStopwatch] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [timeInterval, setTimeInterval] = useState(null);

  useEffect(() => {
    if (startTime) {
      const interval = setInterval(getShowTime, 100);
      setTimeInterval(interval);
    }
  }, [startTime]);

  const firestoreSetStart = (isStart) => {
    projectFirestore
      .collection("variables")
      .doc("start")
      .set({ isStarted: isStart })
      .catch((error) => {
        console.log(error);
      });
  };

  const startStopwatch = () => {
    const newStartTime = new Date().getTime();
    setStartTime(newStartTime);
    firestoreSetStart(true);
  };

  const getShowTime = () => {
    const currentTime = new Date().getTime();
    const difference = parseInt((currentTime - startTime) / 1000);
    setStopwatch(difference);
  };

  const stopStopwatch = () => {
    clearInterval(timeInterval);
    firestoreSetStart(false);
    setStartTime(null);
    setStopwatch(0);
  };

  return (
    <AppContext.Provider value={{ stopwatch, startStopwatch, stopStopwatch }}>
      {children}
    </AppContext.Provider>
  );
};

export const useGlobalContext = () => {
  return useContext(AppContext);
};

export { AppContext, AppProvider };
