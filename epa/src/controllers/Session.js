import axios from 'axios';
import { useEffect } from "react";

export function Session() {

    // Ensure user has a guest session
    useEffect(() => {
        const checkSession = async () => {
            try {
                const response = await axios.get('/get-session', {
                    withCredentials: true, // Ensures cookies are sent
                });
                console.log(response.data.message); // Debug: Check session info
            } catch (error) {
                console.error("Failed to check or create session", error);
            }
        };

        checkSession();
    }, []);

    return;
};
