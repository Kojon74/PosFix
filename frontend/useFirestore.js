import { useState, useEffect } from "react";
import { projectFirestore } from "./firebase";
import { useGlobalContext } from "./context";

const useFirestore = (collection) => {
  const [docs, setDocs] = useState();

  useEffect(() => {
    const unsub = projectFirestore.collection(collection).onSnapshot((snap) => {
      let documents = [];
      snap.forEach((doc) => {
        documents.push({ ...doc.data(), id: doc.id });
      });
      setDocs(documents[documents.length - 1]);
    });
    return () => unsub();
  }, [collection]);
  return { docs };
};
export default useFirestore;
