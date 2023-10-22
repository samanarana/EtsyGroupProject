import React, { useState, useMemo } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart as solidHeart } from '@fortawesome/free-solid-svg-icons';
import { faHeart as regularHeart } from '@fortawesome/free-regular-svg-icons';
import { Link } from 'react-router-dom';
import './ProductTile.css';
import { addFavoriteThunk, removeFavoriteThunk } from './../../store/favorite';

const ProductTile = ({ product: { id, imgUrl, productName, avgRating, reviewCount, price } }) => {
    const dispatch = useDispatch();
    const userId = useSelector(state => state.session.user.id);
    const favorites = useSelector(state => state.favorite.favorites);

    const isProductFavorited = useMemo(() => {
        return favorites.some(favorite => favorite.productId === id);
    }, [favorites, id]);

    const [isFavorited, setIsFavorited] = useState(isProductFavorited);

    const handleHeartClick = (event) => {
        event.stopPropagation();
        event.preventDefault();

        if (isFavorited) {
            dispatch(removeFavoriteThunk(userId, id));
        } else {
            dispatch(addFavoriteThunk(userId, id));
        }

        setIsFavorited(!isFavorited);
    };

    return (
        <Link to={`/products/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className='product-tile'>
                <div className="image-wrapper">
                    {imgUrl ?
                        <img src={imgUrl} alt={productName} />
                        :
                        <div className="image-placeholder"></div>
                    }
                    <button className='favorite-btn' onClick={handleHeartClick}>
                        {isFavorited ?
                            <FontAwesomeIcon icon={solidHeart} style={{color: "#c70000"}} />
                            :
                            <FontAwesomeIcon icon={regularHeart} style={{color: "#000000"}} />
                        }
                    </button>
                </div>
                <div className="product-details">
                    <div className='product-name'>{productName}</div>
                    <div className='product-rating'>
                        ★ {avgRating} ({reviewCount})
                    </div>
                    <div className='product-price'>{`$${price}`}</div>
                    <button className='add-to-cart-btn'>+ Add to cart</button>
                </div>
            </div>
        </Link>
    );
}

export default ProductTile;
