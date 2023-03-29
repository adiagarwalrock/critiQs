import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MovieList() {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        axios.get('movies/')
            .then(response => setMovies(response.data))
            .catch(error => console.error(error));
    }, []);

    return (
        <div>
            <h1>Movie List</h1>
            <ul>
                {movies.map(movie => (
                    <li key={movie.id}>{movie.title}</li>
                ))}
            </ul>
        </div>
    );
}

export default MovieList;
