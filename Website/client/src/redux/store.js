import {configureStore, combineReducers} from "@reduxjs/toolkit";
import useReducer from "./user/userSlice.js";
import {persistReducer, persistStore} from "redux-persist";
import sessionStorage from "redux-persist/es/storage/session";

const rootReducer = combineReducers({user: useReducer});

const persistConfig = {
  key: 'root',
  storage: sessionStorage,
  version: 1,
}

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export const persistor = persistStore(store);